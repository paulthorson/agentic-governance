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

# ---------------------------------------------------------------------------
# Framework discovery
# ---------------------------------------------------------------------------

REPO_ROOT = Path(os.environ.get("ADVERSARIAL_ROOT", Path.home() / "adversarial-agents"))
DOMAINS = ["ux", "engineer", "qa", "researcher", "universal", "prompt", "security", "privacy", "compliance", "product"]
DOMAIN_DIR = {d: REPO_ROOT / f"adversarial-{d}" for d in DOMAINS}

RUNS_DIR = REPO_ROOT / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
VERDICT_LOG = RUNS_DIR / "verdicts.jsonl"


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
    return _read(DOMAIN_DIR.get(domain, Path()) / "references" / "constitution.md")


def _standard(domain: str) -> str:
    return _read(DOMAIN_DIR.get(domain, Path()) / "references" / "standard.md")


def _personas(domain: str) -> str:
    return _read(DOMAIN_DIR.get(domain, Path()) / "references" / "personas.md")


def _ledger(domain: str) -> str:
    return _read(DOMAIN_DIR.get(domain, Path()) / "references" / "calibration-ledger.md")


# ---------------------------------------------------------------------------
# Verdict / decision-record persistence
# ---------------------------------------------------------------------------


def _append_verdict(record: dict[str, Any]) -> None:
    record.setdefault("ts", int(time.time() * 1000))
    with VERDICT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def _load_verdicts(domain: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
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
        rows.append(r)
    return rows[-limit:]


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
def run_review(domain: str, work: str, context: str = "") -> dict[str, Any]:
    """Run a governed adversarial review on a piece of work.

    Args:
        domain: one of ux, engineer, qa, researcher, universal.
        work: the artifact/decision/claim to review (code, design, plan, message, research).
        context: optional surrounding context (ticket, constraints, prior findings).

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
def record_verdict(domain: str, verdict: str, summary: str, ticket: str = "") -> dict[str, Any]:
    """Record a review verdict to the decision record (calibration ledger).

    Args:
        domain: the domain reviewed.
        verdict: KICK_BACK or ALLOW.
        summary: short human summary of the outcome.
        ticket: optional ticket/issue id.
    """
    rec = {
        "kind": "verdict",
        "domain": domain,
        "verdict": verdict.upper(),
        "summary": summary,
        "ticket": ticket,
    }
    _append_verdict(rec)
    return {"recorded": True, "record": rec}


@mcp.tool()
def query_verdicts(domain: str = "", limit: int = 50) -> list[dict[str, Any]]:
    """Query recent review verdicts from the decision record. Optionally filter by domain."""
    return _load_verdicts(domain or None, limit)


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
