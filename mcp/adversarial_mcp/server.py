"""Adversarial Agents MCP server.

Exposes the adversarial review framework as callable MCP tools so any agent
(Claude, Cursor, OpenClaw, or a custom client) can run a governed review,
check a hard veto, record/query verdicts, and inventory the framework.

The server reads the framework directly from the repo layout:

    ~/adversarial-agents/
      adversarial-<domain>/          # plugin source of truth
        agents/*.md                  # adversary agent definitions
        skills/*/SKILL.md            # stateless skills
        references/constitution.md   # constitutional rules
        references/calibration-ledger.md
      agents/                        # flat namespaced agents (ux-critic, eng-...)
      skills/                        # flat namespaced skills (ux-altitude-check, ...)

Verdicts are appended to a JSONL decision record under runs/ (gitignored), so
real review history never gets committed.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import setup_wizard

# ---------------------------------------------------------------------------
# Framework discovery
# ---------------------------------------------------------------------------

# Repo root resolves from this file's own location (mcp/adversarial_mcp/server.py
# → up two parents to the repo root) so the repo can be renamed or cloned
# anywhere without breaking. ADVERSARIAL_ROOT overrides when set.
REPO_ROOT = Path(os.environ.get("ADVERSARIAL_ROOT", Path(__file__).resolve().parents[2]))
DOMAINS = ["ux", "engineer", "qa", "researcher", "universal", "prompt", "security", "privacy", "compliance", "product", "ops", "docs"]
DOMAIN_DIR = {d: REPO_ROOT / f"adversarial-{d}" for d in DOMAINS}

RUNS_DIR = REPO_ROOT / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
VERDICT_LOG = RUNS_DIR / "verdicts.jsonl"

# A21: retention window (days) for the calibration ledger. Entries older than
# this are summarized to a stub on load (age-out). The operator sets this;
# default 90 days.
RETENTION_DAYS = int(os.environ.get("LEDGER_RETENTION_DAYS", "90"))


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _frontmatter(text: str) -> dict[str, Any]:
    """Parse YAML-ish frontmatter (name:, description:, etc.) leniently."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    out: dict[str, Any] = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _agents_for(domain: str) -> list[dict[str, str]]:
    d = DOMAIN_DIR.get(domain)
    if not d:
        return []
    out = []
    for f in sorted((d / "agents").glob("*.md")):
        text = _read(f)
        fm = _frontmatter(text)
        out.append(
            {
                "name": fm.get("name", f.stem),
                "file": f.name,
                "description": fm.get("description", ""),
                "body": text,
            }
        )
    return out


def _skills_for(domain: str) -> list[dict[str, str]]:
    d = DOMAIN_DIR.get(domain)
    if not d:
        return []
    out = []
    for f in sorted((d / "skills").glob("*/SKILL.md")):
        text = _read(f)
        fm = _frontmatter(text)
        out.append(
            {
                "name": fm.get("name", f.parent.name),
                "dir": f.parent.name,
                "description": fm.get("description", ""),
                "body": text,
            }
        )
    return out


def _constitution(domain: str) -> str:
    # Per-domain constitutions live in constitution/domains/<domain>.md
    # (moved out of capability folders). See the governance restructure changelog.
    return _read(REPO_ROOT / "constitution" / "domains" / f"{domain}.md")


def _standard(domain: str) -> str:
    # Each plugin ships exactly one standard file under references/ with a
    # domain-specific name. Glob for it and require exactly one match; on zero
    # or several, return an explicit error naming the domain (never silent-empty).
    refs_dir = DOMAIN_DIR.get(domain, Path()) / "references"
    candidates = [
        p for p in sorted(refs_dir.glob("*.md"))
        if p.name not in ("calibration-ledger.md", "personas.md")
    ]
    if len(candidates) == 1:
        return candidates[0].read_text(encoding="utf-8", errors="replace")
    names = [p.name for p in candidates]
    if len(candidates) == 0:
        return f"<STANDARD MISSING for domain '{domain}': no standard file found in {refs_dir}>"
    return (f"<STANDARD AMBIGUOUS for domain '{domain}': expected exactly one standard "
            f"file in {refs_dir}, found {len(candidates)}: {', '.join(names)}>")


def _personas(domain: str) -> str:
    return _read(DOMAIN_DIR.get(domain, Path()) / "references" / "personas.md")


def _ledger(domain: str) -> str:
    return _read(DOMAIN_DIR.get(domain, Path()) / "references" / "calibration-ledger.md")


# ---------------------------------------------------------------------------
# Verdict / decision-record persistence
# ---------------------------------------------------------------------------


def _append_verdict(record: dict[str, Any]) -> None:
    record.setdefault("ts", int(time.time() * 1000))
    # A22: every ruling carries a status (active by default) and a provenance
    # field linking the artifact to the ruling that permitted it.
    record.setdefault("status", "active")
    record.setdefault("provenance", "")
    with VERDICT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def _load_verdicts(domain: str | None = None, limit: int = 50, source: str | None = None) -> list[dict[str, Any]]:
    if not VERDICT_LOG.exists():
        return []
    rows = []
    for line in VERDICT_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if domain and r.get("domain") != domain:
            continue
        if source is not None and r.get("source") != source:
            continue
        rows.append(r)
    # A21 age-out: entries older than the retention window are summarized to a
    # stub (kept, but flagged) so the ledger does not grow without bound. The
    # retention window is in days; the operator sets it (default 90).
    rows = [_age_out(r) for r in rows]
    return rows[-limit:]


def _age_out(record: dict[str, Any]) -> dict[str, Any]:
    """A21: summarize an entry older than the retention window to a stub.

    The full record is retained on disk (append-only); the stub is what a
    consumer sees for old entries, so the load cost stays bounded while the
    history is preserved.
    """
    ts = record.get("ts")
    if not ts:
        return record
    age_days = (time.time() * 1000 - ts) / 86400000.0
    if age_days <= RETENTION_DAYS:
        return record
    return {
        "kind": record.get("kind", "verdict"),
        "domain": record.get("domain", ""),
        "verdict": record.get("verdict", ""),
        "summary": "[aged out] " + (record.get("summary", "") or "")[:80],
        "ticket": record.get("ticket", ""),
        "rule": record.get("rule", ""),
        "case_tag": record.get("case_tag", ""),
        "ts": ts,
        "aged_out": True,
    }


# ---------------------------------------------------------------------------
# Review engine (deterministic structural checks + prompt assembly)
# ---------------------------------------------------------------------------

VETO_KEYWORDS = {
    "ux": [
        "dead end", "accessibility impossible", "silent divergence", "data loss",
        "money loss", "user harm", "screen reader", "no keyboard access",
    ],
    "engineer": [
        "data loss", "security hole", "bricked config", "production outage",
        "credential leak", "security breach", "api key", "secret exposed",
        "leak credential", "expose secret", "sql injection", "remote code execution",
        "privilege escalation", "downtime", "rollback impossible",
    ],
    "qa": [
        "user harm", "data loss", "money loss", "release-blocking defect",
        "crash on launch", "data corruption", "security regression",
    ],
    "researcher": [
        "unsupported claim", "fabricated user", "causal claim from correlation",
        "no source", "made up data", "fabricated data", "no evidence",
    ],
    "universal": [
        "irrecoverable harm", "data loss", "security breach", "credential leak",
        "safety", "api key", "secret exposed", "privacy violation", "legal liability",
    ],
    "prompt": [
        "injected instruction", "safety override", "clear a veto", "exfiltrate data",
        "ignore previous instructions", "role override", "loyalty shift",
        "secret exfiltration", "bypass the human gate",
    ],
    "security": [
        "exploitable vulnerability", "secret exposure", "credential leak", "api key",
        "sql injection", "remote code execution", "privilege escalation", "auth bypass",
        "critical cve", "untrusted dependency", "sensitive data exposed",
    ],
    "privacy": [
        "unlawful data collection", "no consent", "unbounded retention",
        "no subject rights", "unlawful transfer", "pii exposed", "gdpr violation",
        "ccpa violation",
    ],
    "compliance": [
        "regulatory violation", "policy violation", "no evidence of compliance",
        "no audit trail", "non-compliant", "legal liability",
    ],
    "product": [
        "unvalidated market assumption", "fabricated user need",
        "unsupported competitive claim", "unsound business case", "market risk",
    ],
    "ops": [
        "irreversible deployment", "no rollback path", "no disaster recovery",
        "unobservable in production", "downtime", "data loss",
    ],
    "docs": [
        "factually wrong documentation", "missing critical documentation",
        "misleading documentation", "outdated documentation",
    ],
}

# Regex patterns for credential/secret exposure that keyword matching misses.
VETO_PATTERNS = {
    "engineer": [r"(expos|leak|commit).{0,20}(api[ -]?key|secret|credential|token|password)",
                  r"(api[ -]?key|secret|credential|token|password).{0,20}(expos|leak|log|commit)"],
    "universal": [r"(expos|leak).{0,20}(api[ -]?key|secret|credential|token|password)"],
}


def _veto_hits(domain: str, text: str) -> list[str]:
    import re as _re

    text_l = text.lower()
    hits = [k for k in VETO_KEYWORDS.get(domain, []) if k in text_l]
    for pat in VETO_PATTERNS.get(domain, []):
        if _re.search(pat, text_l):
            hits.append(f"pattern:{pat}")
    return hits


def _run_structural_review(domain: str, work: str) -> dict[str, Any]:
    """Deterministic first pass: veto scan + basic completeness checks."""
    hits = _veto_hits(domain, work)
    agents = _agents_for(domain)
    return {
        "domain": domain,
        "veto_hits": hits,
        "veto_triggered": bool(hits),
        "agent_count": len(agents),
        "agents": [a["name"] for a in agents],
        "work_chars": len(work),
    }


# ---------------------------------------------------------------------------
# MCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("adversarial-agents")


@mcp.tool()
def setup_wizard_start() -> dict[str, Any]:
    """Begin (or resume) the conversational governance setup wizard (Section 9.3).
    Returns the first/pending question, with labeled options where bounded. Call
    setup_wizard_answer() with the operator's reply."""
    return setup_wizard.start_wizard(REPO_ROOT)


@mcp.tool()
def setup_wizard_answer(answer: str) -> dict[str, Any]:
    """Record the operator's answer to the current wizard question and return the
    next question, or the completion summary when the wizard is done. For bounded
    questions, answer must be one of the offered options; for roster rows, send
    'done' to finish the roster. Writes config/setup.md, config/roster.md, and one
    persona block per roster row into config/personas/ on completion."""
    return setup_wizard.answer_wizard(REPO_ROOT, answer)


@mcp.tool()
def list_domains() -> list[str]:
    """List the adversarial domains available (ux, engineer, qa, researcher, universal)."""
    return DOMAINS


@mcp.tool()
def list_agents(domain: str) -> list[dict[str, str]]:
    """List the adversary agents for a domain (e.g. 'ux' -> ux-critic, ux-cx-advocate, ...)."""
    return [{"name": a["name"], "description": a["description"]} for a in _agents_for(domain)]


@mcp.tool()
def list_skills(domain: str) -> list[dict[str, str]]:
    """List the stateless skills available for a domain."""
    return [{"name": s["name"], "description": s["description"]} for s in _skills_for(domain)]


@mcp.tool()
def get_constitution(domain: str) -> str:
    """Return the constitutional rules (hard gates) for a domain."""
    return _constitution(domain) or f"No constitution found for domain '{domain}'."


@mcp.tool()
def get_standard(domain: str) -> str:
    """Return the domain standard (quality bar) for a domain."""
    return _standard(domain) or f"No standard found for domain '{domain}'."


@mcp.tool()
def get_agent(domain: str, agent_name: str) -> str:
    """Return the full body of a specific adversary agent (e.g. domain='ux', agent_name='ux-critic')."""
    for a in _agents_for(domain):
        if a["name"] == agent_name or a["file"].startswith(agent_name):
            return a["body"]
    return f"Agent '{agent_name}' not found in domain '{domain}'."


@mcp.tool()
def run_review(domain: str, work: str, context: str = "", source: str = "app") -> dict[str, Any]:
    """Run a governed adversarial review on a piece of work.

    Args:
        domain: one of ux, engineer, qa, researcher, universal.
        work: the artifact/decision/claim to review (code, design, plan, message, research).
        context: optional surrounding context (ticket, constraints, prior findings).
        source: provenance tag for the verdict log — "app" for real reviews, or a
            test/automation tag (e.g. "smoke_test") so records can be filtered out.

    Returns a structured verdict: structural scan, veto status, and the review
    prompt assembled for the domain's adversary agents.
    """
    structural = _run_structural_review(domain, work)
    agents = _agents_for(domain)
    constitution = _constitution(domain)

    review_prompt = (
        f"# Adversarial review — domain: {domain}\n\n"
        f"## Work under review\n{work}\n\n"
        f"## Context\n{context or '(none provided)'}\n\n"
        f"## Constitutional rules\n{constitution or '(none)'}\n\n"
        f"## Adversary agents to run\n"
        + "\n".join(f"- {a['name']}: {a['description']}" for a in agents)
        + "\n\nFor each agent, produce: findings, severity (blocker/major/minor/nit), "
        "and a verdict of KICK_BACK or ALLOW. If any agent finds a blocker or a "
        "constitutional veto is triggered, the overall verdict is KICK_BACK."
    )

    verdict = "KICK_BACK" if structural["veto_triggered"] else "REVIEW_REQUIRED"
    result = {
        "domain": domain,
        "verdict": verdict,
        "veto_triggered": structural["veto_triggered"],
        "veto_hits": structural["veto_hits"],
        "agents": structural["agents"],
        "review_prompt": review_prompt,
    }
    _append_verdict(
        {
            "kind": "review",
            "domain": domain,
            "verdict": verdict,
            "veto_hits": structural["veto_hits"],
            "work_chars": structural["work_chars"],
            "rule": "constitution-rule-1" if structural["veto_triggered"] else "",
            "case_tag": "veto" if structural["veto_triggered"] else "review",
            "source": source,
        }
    )
    return result


# ---------------------------------------------------------------------------
# Deep review (LLM-invoked)
# ---------------------------------------------------------------------------

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEEP_MODEL = os.environ.get("ADVERSARIAL_DEEP_MODEL", "gemma3:12b")


def _ollama_generate(prompt: str, model: str | None = None) -> str:
    """Call Ollama to run the adversary agents on the assembled prompt."""
    import urllib.request

    payload = json.dumps(
        {
            "model": model or DEEP_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 8192},
        }
    ).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
        return data.get("response", "")
    except Exception as e:
        return f"ERROR: deep review failed: {e}"


@mcp.tool()
def run_review_deep(domain: str, work: str, context: str = "", model: str = "") -> dict[str, Any]:
    """Run a governed adversarial review, invoking the adversary agents via an LLM.

    Unlike run_review (which assembles the prompt), this actually calls the LLM
    to execute the domain's adversary agents and returns their findings.

    Args:
        domain: one of the adversarial domains.
        work: the artifact/decision/claim to review.
        context: optional surrounding context.
        model: optional Ollama model override (default gemma3:12b).

    Returns the structural scan plus the LLM-generated verdict and findings.
    """
    structural = _run_structural_review(domain, work)
    agents = _agents_for(domain)
    constitution = _constitution(domain)
    standard = _standard(domain)

    prompt = (
        f"You are the adversarial review team for the '{domain}' domain.\n\n"
        f"## Work under review\n{work}\n\n"
        f"## Context\n{context or '(none provided)'}\n\n"
        f"## Constitution\n{constitution or '(none)'}\n\n"
        f"## Standard\n{standard or '(none)'}\n\n"
        f"## Adversary agents\n"
        + "\n".join(f"- {a['name']}: {a['description']}" for a in agents)
        + "\n\nFor each agent, produce findings with severity "
        "(BLOCKER/CONCERN/NOTE) and a verdict of KICK_BACK or ALLOW. "
        "If any agent finds a BLOCKER or a constitutional veto is triggered, "
        "the overall verdict is KICK_BACK. End with: VERDICT: KICK_BACK|ALLOW"
    )

    llm_out = _ollama_generate(prompt, model or None)
    llm_lower = llm_out.lower()
    llm_verdict = "KICK_BACK" if "kick_back" in llm_lower else "ALLOW"
    # A structural veto overrides the LLM verdict — the veto is absolute.
    final_verdict = "KICK_BACK" if structural["veto_triggered"] else llm_verdict

    result = {
        "domain": domain,
        "verdict": final_verdict,
        "veto_triggered": structural["veto_triggered"],
        "veto_hits": structural["veto_hits"],
        "agents": structural["agents"],
        "model": model or DEEP_MODEL,
        "llm_findings": llm_out,
    }
    _append_verdict(
        {
            "kind": "deep_review",
            "domain": domain,
            "verdict": final_verdict,
            "veto_hits": structural["veto_hits"],
            "rule": "constitution-rule-1" if structural["veto_triggered"] else "",
            "case_tag": "veto" if structural["veto_triggered"] else "deep_review",
            "model": model or DEEP_MODEL,
        }
    )
    return result


@mcp.tool()
def check_veto(domain: str, text: str) -> dict[str, Any]:
    """Check whether text trips a hard constitutional veto for a domain.

    Returns the triggered veto keywords and a boolean. A veto means only a human
    can clear it — the work must be kicked back.
    """
    hits = _veto_hits(domain, text)
    return {"domain": domain, "veto_triggered": bool(hits), "veto_hits": hits}


@mcp.tool()
def record_verdict(domain: str, verdict: str, summary: str, ticket: str = "", rule: str = "", case_tag: str = "") -> dict[str, Any]:
    """Record a review verdict to the decision record (calibration ledger).

    Args:
        domain: the domain reviewed.
        verdict: KICK_BACK or ALLOW.
        summary: short human summary of the outcome.
        ticket: optional ticket/issue id.
        rule: the rule cited (A21 structured field — e.g. the constitution rule
            or harness section the verdict turns on).
        case_tag: a short case tag for precedent matching (A21 structured
            field — e.g. "veto-production-harm", "two-approaches").
    """
    rec = {
        "kind": "verdict",
        "domain": domain,
        "verdict": verdict.upper(),
        "summary": summary,
        "ticket": ticket,
        "rule": rule,
        "case_tag": case_tag,
        "source": "app",
    }
    _append_verdict(rec)
    return {"recorded": True, "record": rec}


@mcp.tool()
def query_verdicts(domain: str = "", limit: int = 50, source: str = "") -> list[dict[str, Any]]:
    """Query recent review verdicts from the decision record. Optionally filter by
    domain and/or source (e.g. source="app" for real reviews, source="smoke_test"
    to inspect test records). An empty source filter matches all sources."""
    return _load_verdicts(domain or None, limit, source or None)


@mcp.tool()
def overturn_verdict(ticket: str, reason: str) -> dict[str, Any]:
    """A22: mark a ruling as overturned (status, not deletion).

    Only a human overturns a precedent (matching who clears a veto). The ruling
    keeps its record but is flagged `overturned` so it is no longer citable as
    precedent — a bot that would have cited it must instead escalate (the
    overturned status makes the match "arguable," which already means escalate
    under 10.1).

    Args:
        ticket: the ticket/issue id of the ruling to overturn.
        reason: why it is overturned (recorded for the audit trail).
    """
    if not ticket or not reason:
        return {"status": "error", "error": "ticket and reason are required."}
    if not VERDICT_LOG.exists():
        return {"status": "error", "error": "No verdict log to overturn from."}
    lines = VERDICT_LOG.read_text(encoding="utf-8").splitlines()
    found = False
    out = []
    for line in lines:
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            out.append(line)
            continue
        if r.get("ticket") == ticket and r.get("status") != "overturned":
            r["status"] = "overturned"
            r["overturned_at"] = int(time.time() * 1000)
            r["overturned_reason"] = reason
            found = True
        out.append(json.dumps(r))
    if not found:
        return {"status": "error", "error": f"No active ruling found for ticket '{ticket}'."}
    VERDICT_LOG.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {"status": "overturned", "ticket": ticket, "reason": reason}


@mcp.tool()
def framework_status() -> dict[str, Any]:
    """Return a health summary of the framework: domains, agent/skill counts, verdict log size."""
    return {
        "root": str(REPO_ROOT),
        "domains": DOMAINS,
        "agents_per_domain": {d: len(_agents_for(d)) for d in DOMAINS},
        "skills_per_domain": {d: len(_skills_for(d)) for d in DOMAINS},
        "verdict_log": str(VERDICT_LOG),
        "verdict_count": sum(1 for _ in VERDICT_LOG.open() if _.strip()) if VERDICT_LOG.exists() else 0,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
