"""
setup_wizard.py — Conversational setup wizard for agentic governance.

Per Section 9 of the ratified spec (docs/agentic-governance-spec.md):

- The wizard is CONVERSATIONAL, not a script. It is exposed through the MCP
  server as tools the operator's agent invokes. Questions are asked natively
  in whatever tool the operator is using, with labeled options wherever the
  answer set is bounded. Nothing is filled in by hand; no config file is
  authored manually.
- Answers are written to config/setup.md and config/roster.md.
- The final step generates one persona block per roster row into
  config/personas/ (Section 9.4 template).
- It is re-runnable. Absent or incomplete config is the UNKNOWN state; the
  wizard never defaults a value.

State machine: two MCP tools drive it.
  - setup_wizard_start()   -> begins (or resumes) the wizard, returns the
                              first (or next pending) question.
  - setup_wizard_answer(v) -> records the answer to the current question and
                              returns the next question, or the completion
                              summary when all questions are done.

State is persisted to config/.wizard-state.json so a long-running or restarted
server can resume mid-wizard, and so an incomplete config is never mistaken
for a complete one.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# --- constants ---------------------------------------------------------------

BUDGET_MODELS = ["metered", "billed", "not-yet-known"]
ADVERSARIAL_STATES = ["in-play", "not-in-play"]

# The question flow. Each entry:
#   id        – stable key under which the answer is stored
#   question  – the prompt shown to the operator
#   options   – None for free text, else a list of labeled choices
#   repeated  – True for roster rows (asked until the operator sends "done")
WIZARD_FLOW: list[dict[str, Any]] = [
    {
        "id": "runtime",
        "question": "What executes the agents? (Name your runtime. This determines only the persona block wrapper, never the content.)",
        "options": None,
    },
    {
        "id": "budget_model",
        "question": "What is the budget model?",
        "options": BUDGET_MODELS,
    },
    # conditional sub-questions (only presented when budget_model == their key)
    {
        "id": "metered_allowance",
        "if_budget": "metered",
        "question": "Metered: what is the allowance per cycle?",
        "options": None,
    },
    {
        "id": "metered_reset_cadence",
        "if_budget": "metered",
        "question": "Metered: what is the reset cadence (e.g. weekly)?",
        "options": None,
    },
    {
        "id": "metered_headroom",
        "if_budget": "metered",
        "question": "Metered: how much headroom should the CEO reserve for in-flight work?",
        "options": None,
    },
    {
        "id": "billed_cap",
        "if_budget": "billed",
        "question": "Billed: what is the total spend cap?",
        "options": None,
    },
    {
        "id": "billed_escalation_threshold",
        "if_budget": "billed",
        "question": "Billed: at what percentage of the cap should escalation trigger?",
        "options": None,
    },
    {
        "id": "per_epic_budget",
        "question": "What is a single epic allowed to consume?",
        "options": None,
    },
    {
        "id": "roster",
        "question": "Add a roster row as: bot name | role | team | default project repo(s). Send 'done' when the roster is complete.",
        "options": None,
        "repeated": True,
    },
    {
        "id": "adversarial_agents",
        "question": "Are the adversarial agents in play?",
        "options": ADVERSARIAL_STATES,
    },
    {
        "id": "project_repos",
        "question": "Where do project repos live, and what is the epic folder convention?",
        "options": None,
    },
    {
        "id": "escalation_preferences",
        "question": "Which escalation categories should always reach the human beyond the mandatory list in Section 10.3?",
        "options": None,
    },
    {
        "id": "domain_risk",
        "question": "Are there industry or regulatory constraints making certain decisions non-delegable? (This is the only place domain specificity may enter.)",
        "options": None,
    },
    {
        "id": "quiet_hours",
        "question": "When is the human unavailable? (Escalations in this window queue rather than stall.)",
        "options": None,
    },
    {
        "id": "stall_threshold",
        "question": "How many turns without a materially new artifact before a blocked case is queued?",
        "options": None,
    },
    {
        "id": "precedent_decay_window",
        "question": "How old can a precedent be before it is flagged for fresh review rather than applied automatically?",
        "options": None,
    },
]

# --- state persistence -------------------------------------------------------

WIZARD_STATE_FILE = "wizard-state.json"  # resolved under config/


def _state_path(repo_root: Path) -> Path:
    return repo_root / "config" / WIZARD_STATE_FILE


def _load_state(repo_root: Path) -> dict[str, Any]:
    p = _state_path(repo_root)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(repo_root: Path, state: dict[str, Any]) -> None:
    p = _state_path(repo_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2), encoding="utf-8")


# --- helpers -----------------------------------------------------------------

def _is_repeated_pending(state: dict[str, Any], q: dict[str, Any]) -> bool:
    """A repeated question (roster) is complete when the last recorded value
    for its id was the 'done' sentinel."""
    return state.get(q["id"], [])[-1:] != ["__DONE__"]


def _enabled(q: dict[str, Any], answers: dict[str, Any]) -> bool:
    """A question with if_budget is shown only when the budget model matches."""
    cond = q.get("if_budget")
    if cond is None:
        return True
    return answers.get("budget_model") == cond


def _next_question(state: dict[str, Any]) -> dict[str, Any] | None:
    answers = state.get("answers", {})
    flow = state.get("flow_index", 0)
    # advance past any disabled or already-answered questions
    while flow < len(WIZARD_FLOW):
        q = WIZARD_FLOW[flow]
        if not _enabled(q, answers):
            flow += 1
            continue
        if q.get("repeated"):
            # repeated question stays current until 'done' recorded
            if _is_repeated_pending(state, q):
                break
            flow += 1
            continue
        if q["id"] in answers:
            flow += 1
            continue
        break
    if flow >= len(WIZARD_FLOW):
        return None
    state["flow_index"] = flow
    return WIZARD_FLOW[flow]


def _current_question(state: dict[str, Any]) -> dict[str, Any] | None:
    flow = state.get("flow_index", 0)
    if flow >= len(WIZARD_FLOW):
        return None
    q = WIZARD_FLOW[flow]
    if not _enabled(q, state.get("answers", {})):
        return None
    return q


# --- config writers ----------------------------------------------------------

def _write_setup(repo_root: Path, answers: dict[str, Any]) -> Path:
    p = repo_root / "config" / "setup.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Setup",
        "",
        "Configured by the conversational setup wizard (Section 9.3). "
        "Absent or incomplete config is the unknown state; the CEO bot does not "
        "start work on unknown and re-runs the wizard instead.",
        "",
        "## Runtime",
        f"- {answers.get('runtime', '') or '(unset)'}",
        "",
        "## Budget model",
        f"- {answers.get('budget_model', '') or '(unset)'}",
    ]
    model = answers.get("budget_model")
    if model == "metered":
        lines += [
            "",
            "### Metered",
            f"- allowance per cycle: {answers.get('metered_allowance', '') or '(unset)'}",
            f"- reset cadence: {answers.get('metered_reset_cadence', '') or '(unset)'}",
            f"- headroom reserved for in-flight work: {answers.get('metered_headroom', '') or '(unset)'}",
        ]
    elif model == "billed":
        lines += [
            "",
            "### Billed",
            f"- total spend cap: {answers.get('billed_cap', '') or '(unset)'}",
            f"- escalation threshold (% of cap): {answers.get('billed_escalation_threshold', '') or '(unset)'}",
        ]
    lines += [
        "",
        "## Per-epic budget",
        f"- {answers.get('per_epic_budget', '') or '(unset)'}",
        "",
        "## Adversarial agents",
        f"- in play: {answers.get('adversarial_agents', '') or '(unset)'}",
        "",
        "## Project repos",
        f"- {answers.get('project_repos', '') or '(unset)'}",
        "",
        "## Escalation preferences (beyond Section 10.3 mandatory list)",
        f"- {answers.get('escalation_preferences', '') or '(unset)'}",
        "",
        "## Domain risk",
        f"- {answers.get('domain_risk', '') or '(unset)'}",
        "",
        "## Quiet hours",
        f"- {answers.get('quiet_hours', '') or '(unset)'}",
        "",
        "## Stall threshold",
        f"- {answers.get('stall_threshold', '') or '(unset)'}",
        "",
        "## Precedent decay window",
        f"- {answers.get('precedent_decay_window', '') or '(unset)'}",
        "",
    ]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def _write_roster(repo_root: Path, roster: list[list[str]]) -> Path:
    p = repo_root / "config" / "roster.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Roster",
        "",
        "Every bot in the system, one row per bot. A bot finds its own row by its name.",
        "",
        "| Bot name | Role | Team | Default project repo(s) |",
        "|---|---|---|---|",
    ]
    for row in roster:
        while len(row) < 4:
            row.append("")
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def _write_personas(repo_root: Path, roster: list[list[str]], answers: dict[str, Any]) -> list[Path]:
    personas_dir = repo_root / "config" / "personas"
    personas_dir.mkdir(parents=True, exist_ok=True)
    runtime = answers.get("runtime", "runtime")
    governance_repo = "agentic-governance"  # canonical governance repo name
    written: list[Path] = []
    for row in roster:
        bot_name, role, team, repo = (row + ["", "", "", ""])[:4]
        if not bot_name:
            continue
        block = (
            f"You are {bot_name}, the {role} bot for {team}.\n\n"
            f"Before every task, read the following from {governance_repo}:\n"
            f"  - constitution/constitution.md\n"
            f"  - harnesses/{role}.md\n"
            f"  - config/setup.md\n"
            f"  - config/roster.md\n\n"
            f"Your harness defines what you own, what you never do, who you receive from,\n"
            f"who you hand to, the artifact format you must produce, and when to stop.\n"
            f"It overrides anything in this block.\n\n"
            f"{governance_repo} is READ-ONLY to you. A commit from you to it is a\n"
            f"violation, not a correction.\n\n"
            f"Your default project repo is {repo}, unless your assignment names another.\n"
            f"You write only to your own folder in the epic you were handed.\n"
        )
        # one persona block per roster row; the runtime is the (thin) wrapper
        filename = "".join(c if c.isalnum() or c in "-_" else "_" for c in bot_name.lower())
        p = personas_dir / f"{filename}.md"
        p.write_text(f"# {bot_name}\n\nRuntime wrapper: {runtime}\n\n{block}", encoding="utf-8")
        written.append(p)
    return written


# --- orchestration -----------------------------------------------------------

def start_wizard(repo_root: Path) -> dict[str, Any]:
    """Begin (or resume) the wizard. Returns the first/pending question."""
    state = _load_state(repo_root)
    if not state:
        state = {"flow_index": 0, "answers": {}, "roster": []}
        _save_state(repo_root, state)
    q = _next_question(state)
    if q is None:
        return _finalize(repo_root, state)
    _save_state(repo_root, state)
    return _question_payload(q, len(state.get("roster", [])))


def answer_wizard(repo_root: Path, value: str) -> dict[str, Any]:
    """Record the answer to the current question; return the next question or
    the completion summary."""
    state = _load_state(repo_root)
    if not state:
        return {
            "status": "error",
            "error": "No wizard in progress. Call setup_wizard_start() first.",
        }
    q = _current_question(state)
    if q is None:
        return _finalize(repo_root, state)
    value = (value or "").strip()

    # roster rows are collected conversationally until 'done'
    if q.get("repeated"):
        roster = state.setdefault("roster", [])
        if value.lower() == "done":
            # mark roster complete; move on
            state["answers"][q["id"]] = "__DONE__"
        else:
            parts = [p.strip() for p in value.split("|")]
            roster.append(parts if any(parts) else [])
        _save_state(repo_root, state)
        nxt = _next_question(state)
        if nxt is None:
            return _finalize(repo_root, state)
        if nxt.get("id") == q["id"]:
            # still collecting roster rows
            return _question_payload(nxt, len(roster))
        _save_state(repo_root, state)
        return _question_payload(nxt, len(roster))

    # validate bounded answers
    if q.get("options") and value not in q["options"]:
        return {
            "status": "invalid",
            "question": q["id"],
            "error": f"'{value}' is not a valid choice.",
            "options": q["options"],
        }

    state["answers"][q["id"]] = value
    _save_state(repo_root, state)
    nxt = _next_question(state)
    if nxt is None:
        return _finalize(repo_root, state)
    _save_state(repo_root, state)
    return _question_payload(nxt, len(state.get("roster", [])))


def _question_payload(q: dict[str, Any], roster_len: int) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "question",
        "question_id": q["id"],
        "question": q["question"],
    }
    if q.get("options"):
        payload["options"] = q["options"]
    payload["free_text"] = q.get("options") is None
    if q.get("repeated"):
        payload["repeated"] = True
        payload["roster_rows_so_far"] = roster_len
    return payload


def _finalize(repo_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    roster = state.get("roster", [])
    answers = state.get("answers", {})
    setup_path = _write_setup(repo_root, answers)
    roster_path = _write_roster(repo_root, roster)
    persona_paths = _write_personas(repo_root, roster, answers)
    # clear wizard state so a fresh run starts over (re-runnable)
    _state_path(repo_root).unlink(missing_ok=True)
    return {
        "status": "complete",
        "wrote": {
            "setup": str(setup_path),
            "roster": str(roster_path),
            "personas": [str(p) for p in persona_paths],
        },
        "roster_rows": len(roster),
        "note": "Wizard complete. Every configured value is the operator's; re-run the wizard to change anything.",
    }
