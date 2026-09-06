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
    # --- Addendum 01 config questions (A2, A3, A4, A12.4, A14) ---
    {
        "id": "autonomy_starting_level",
        "question": "What autonomy starting level should new bots begin at? (A2.4: default is 1; nothing starts above 2 without setting it explicitly.)",
        "options": None,
    },
    {
        "id": "clean_runs_per_promotion",
        "question": "How many clean runs are required for a bot to be promoted up the autonomy ladder? (A2.2)",
        "options": None,
    },
    {
        "id": "retry_count",
        "question": "What is the declared retry count for a bounded retry? (A3.1: how many attempts are allowed, not 'until it works'.)",
        "options": None,
    },
    {
        "id": "retry_escalation_on_exhaustion",
        "question": "What happens when a retry count is exhausted? (A3.1: never silence, never another attempt.)",
        "options": None,
    },
    {
        "id": "audit_cadence",
        "question": "On what cadence should recurring routines report for the routine audit? (A4.1)",
        "options": None,
    },
    {
        "id": "research_rounds_without_findings",
        "question": "How many rounds without new findings should stop the research discovery loop? (A12.4)",
        "options": None,
    },
    {
        "id": "research_round_budget",
        "question": "What is the round budget for the research discovery loop? (A12.4)",
        "options": None,
    },
    {
        "id": "irreversible_action_protection",
        "question": "For each irreversible action class in A1.1, which protection level applies (1 unreachable / 2 intercepted / 3 instructed)? (A14)",
        "options": None,
    },
    # --- Addendum 01 A6: BYOA adoption flow ---
    # Runs after the roster. The operator adopts existing agents (reconcile,
    # never layer) and/or defines roles that do not exist yet.
    {
        "id": "adopt_existing",
        "question": "Adopt an existing agent (BYOA). For each agent you already run, give: name | what it does | role it maps to (pm, ux, engineer, qa, ceo, or new) | path to its current instructions (optional). Send 'done' when you have no more agents to adopt.",
        "options": None,
        "repeated": True,
    },
    {
        "id": "define_new_role",
        "question": "Define a role that does not exist yet (A6.4). Give the role name, or 'none' to skip. The wizard will collect the 8 skeleton fields and generate a harness.",
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
    """A repeated question (roster) is complete when the recorded value for its
    id is the 'done' sentinel. The roster rows are stored in state['roster'] and
    the sentinel in state['answers'][id] as the string '__DONE__'."""
    return state.get("answers", {}).get(q["id"]) != "__DONE__"


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
        "## Autonomy ladder (A2)",
        f"- starting level for new bots: {answers.get('autonomy_starting_level', '') or '(unset)'}",
        f"- clean runs required per promotion: {answers.get('clean_runs_per_promotion', '') or '(unset)'}",
        "",
        "## Retry budgets (A3)",
        f"- retry count: {answers.get('retry_count', '') or '(unset)'}",
        f"- escalation on exhaustion: {answers.get('retry_escalation_on_exhaustion', '') or '(unset)'}",
        "",
        "## Routine audit (A4)",
        f"- audit cadence: {answers.get('audit_cadence', '') or '(unset)'}",
        "",
        "## Research discovery loop (A12.4)",
        f"- rounds without new findings: {answers.get('research_rounds_without_findings', '') or '(unset)'}",
        f"- round budget: {answers.get('research_round_budget', '') or '(unset)'}",
        "",
        "## Irreversible action protection (A14)",
        f"- per action class: {answers.get('irreversible_action_protection', '') or '(unset)'}",
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


# --- A6 BYOA: adoption helpers ----------------------------------------------

# The 9-section harness skeleton (Section 4 of the spec). Used to generate a
# harness for a role that does not exist yet (A6.4).
HARNESS_SKELETON = [
    "## Read first",
    "## Identity",
    "## What you own",
    "## What you never do",
    "## Inputs and who you receive from",
    "## Outputs and who you hand to",
    "## Required artifact format",
    "## Stop conditions",
    "## Permitted plugins",
]

# The 8 fields the wizard collects to define a new role (A6.4).
NEW_ROLE_FIELDS = [
    ("role_identity", "Identity, in one sentence: who this is and what it owns."),
    ("role_never", "What it never does."),
    ("role_receives", "Who it receives work from, and what exact data crosses that edge."),
    ("role_hands_to", "Who it hands to, and what exact data crosses that edge."),
    ("role_artifact", "Its required artifact format."),
    ("role_stop", "Its stop conditions: what makes it stop and escalate rather than proceed."),
    ("role_plugins", "Which plugins it may use (comma-separated)."),
]


def _reconcile_instructions(agent_instructions: str, role: str, repo_root: Path) -> dict[str, Any]:
    """A6.3: sort an existing agent's instructions against the harness for its
    role into covered / compatible-and-specific / conflicting. Never layers.

    This is a best-effort structural reconciliation: it reads the harness for
    the role (if one exists) and the agent's instructions, and classifies each
    instruction line. The operator makes the final call on conflicts.
    """
    harness_path = repo_root / "harnesses" / f"{role}.md"
    harness_text = ""
    if harness_path.exists():
        harness_text = harness_path.read_text(encoding="utf-8")

    # Split the agent's instructions into lines; drop empties and headers.
    lines = [l.strip() for l in agent_instructions.splitlines() if l.strip()]
    covered: list[str] = []
    compatible: list[str] = []
    conflicting: list[str] = []

    for line in lines:
        if line.startswith("#") or line.startswith("---"):
            continue
        low = line.lower()
        # A line that negates something the harness states is a conflict, and
        # must be flagged for the operator BEFORE coverage is considered.
        if _looks_conflicting(low, harness_text):
            conflicting.append(line)
        elif harness_text and any(
            phrase in harness_text.lower()
            for phrase in _key_phrases(low)
        ):
            covered.append(line)
        else:
            compatible.append(line)

    return {
        "role": role,
        "harness": str(harness_path) if harness_path.exists() else None,
        "covered": covered,
        "compatible": compatible,
        "conflicting": conflicting,
        "note": (
            "Reconcile, never layer. Covered lines are dropped (the harness carries "
            "them). Compatible lines move into the harness or persona block. "
            "Conflicting lines go to the operator with both versions shown; the "
            "wizard never resolves a conflict itself."
        ),
    }


def _key_phrases(low: str) -> list[str]:
    """Extract short key phrases from an instruction line for coverage matching."""
    # Drop common filler and keep 3-5 word windows.
    words = [w for w in low.split() if w not in {"the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "you", "your", "must", "should", "always", "never"}]
    phrases: list[str] = []
    for i in range(len(words) - 2):
        phrases.append(" ".join(words[i : i + 3]))
    return phrases


def _looks_conflicting(low: str, harness_text: str) -> bool:
    """Heuristic: a line conflicts if it negates something the harness states.

    A line is conflicting only when it contains a negation AND the harness
    states the positive form of what the line negates (without that same
    negation). A 'never' line that the harness also states (e.g. both say
    'never ship to production without review') is covered, not conflicting.
    """
    if not harness_text:
        return False
    low_h = harness_text.lower()
    for marker in ("never ", "do not ", "must not ", "cannot ", "refuse to "):
        idx = low.find(marker)
        if idx == -1:
            continue
        negated = low[idx + len(marker):].strip()
        # The harness states the positive form of the negated phrase, and does
        # NOT itself carry the same negation marker before that phrase.
        if negated and negated in low_h:
            # Ensure the harness isn't itself negating the same phrase.
            if marker not in low_h[: low_h.find(negated)]:
                return True
    return False


def _generate_harness(role: str, fields: dict[str, str], repo_root: Path) -> Path | None:
    """A6.4/A6.5: generate a harness for a new role from the 9-section skeleton.
    Refuses (returns None) if the harness already exists — never overwrite.
    """
    harness_path = repo_root / "harnesses" / f"{role}.md"
    if harness_path.exists():
        return None  # A6.5: refuse, never overwrite

    lines = [
        f"# {role.title()} Harness",
        "",
        "## Read first",
        "Before beginning any task, load the constitution, this harness file, `config/setup.md`, and the roster. Do this at the start of every task.",
        "",
        "## Identity",
        fields.get("role_identity", ""),
        "",
        "## What you own",
        "",
        "## What you never do",
        fields.get("role_never", ""),
        "",
        "## Inputs and who you receive from",
        fields.get("role_receives", ""),
        "",
        "## Outputs and who you hand to",
        fields.get("role_hands_to", ""),
        "",
        "## Required artifact format",
        fields.get("role_artifact", ""),
        "",
        "## Stop conditions",
        fields.get("role_stop", ""),
        "",
        "## Permitted plugins",
        fields.get("role_plugins", ""),
        "",
    ]
    harness_path.parent.mkdir(parents=True, exist_ok=True)
    harness_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return harness_path


def _answer_adopt_existing(repo_root: Path, state: dict[str, Any], value: str) -> dict[str, Any]:
    """A6.2/A6.3: collect an adopted agent and reconcile its instructions."""
    adopted = state.setdefault("adopted", [])
    if value.lower() == "done":
        state["answers"]["adopt_existing"] = "__DONE__"
        _save_state(repo_root, state)
        nxt = _next_question(state)
        if nxt is None:
            return _finalize(repo_root, state)
        _save_state(repo_root, state)
        return _question_payload(nxt, len(state.get("roster", [])))

    parts = [p.strip() for p in value.split("|")]
    if len(parts) < 2:
        return {
            "status": "invalid",
            "question": "adopt_existing",
            "error": "Format: name | what it does | role | path-to-instructions (optional).",
        }
    name, what = parts[0], parts[1]
    role = parts[2] if len(parts) > 2 and parts[2] else ""
    instr_path = parts[3] if len(parts) > 3 and parts[3] else ""

    # Read the agent's current instructions if a path was given.
    instructions = ""
    if instr_path:
        p = Path(instr_path).expanduser()
        if p.exists():
            instructions = p.read_text(encoding="utf-8")
        else:
            return {
                "status": "invalid",
                "question": "adopt_existing",
                "error": f"Instructions path not found: {instr_path}",
            }

    reconcile = None
    if role and instructions:
        reconcile = _reconcile_instructions(instructions, role, repo_root)

    adopted.append({
        "name": name,
        "what": what,
        "role": role,
        "instructions_path": instr_path,
        "reconcile": reconcile,
    })
    _save_state(repo_root, state)
    nxt = _next_question(state)
    if nxt is None:
        return _finalize(repo_root, state)
    _save_state(repo_root, state)
    return _question_payload(nxt, len(state.get("roster", [])))


def _answer_define_new_role(repo_root: Path, state: dict[str, Any], value: str) -> dict[str, Any]:
    """A6.4: collect the 8 skeleton fields for a new role, then generate a harness."""
    value = (value or "").strip()
    if value.lower() in ("none", "skip", ""):
        state["answers"]["define_new_role"] = "__SKIP__"
        _save_state(repo_root, state)
        nxt = _next_question(state)
        if nxt is None:
            return _finalize(repo_root, state)
        _save_state(repo_root, state)
        return _question_payload(nxt, len(state.get("roster", [])))

    # First answer names the role; subsequent answers fill the 8 fields.
    new_role = state.setdefault("new_role", {})
    if "name" not in new_role:
        new_role["name"] = value
        new_role["field_index"] = 0
        _save_state(repo_root, state)
        field_id, field_q = NEW_ROLE_FIELDS[0]
        return {
            "status": "question",
            "question_id": f"new_role.{field_id}",
            "question": f"For role '{value}': {field_q}",
            "free_text": True,
        }

    # Fill the current field.
    idx = new_role.get("field_index", 0)
    if idx < len(NEW_ROLE_FIELDS):
        field_id, _ = NEW_ROLE_FIELDS[idx]
        new_role[field_id] = value
        new_role["field_index"] = idx + 1
        _save_state(repo_root, state)

    # If more fields remain, ask the next one.
    if new_role.get("field_index", 0) < len(NEW_ROLE_FIELDS):
        nidx = new_role["field_index"]
        field_id, field_q = NEW_ROLE_FIELDS[nidx]
        return {
            "status": "question",
            "question_id": f"new_role.{field_id}",
            "question": f"For role '{new_role['name']}': {field_q}",
            "free_text": True,
        }

    # All fields collected — generate the harness (A6.5: refuse if exists).
    role_name = new_role["name"]
    harness_path = _generate_harness(role_name, new_role, repo_root)
    if harness_path is None:
        return {
            "status": "refused",
            "question": "define_new_role",
            "error": f"A6.5: harness for '{role_name}' already exists at harnesses/{role_name}.md. Refusing to overwrite. Edit the file to amend it.",
        }

    state["answers"]["define_new_role"] = "__DONE__"
    state["generated_harness"] = str(harness_path)
    _save_state(repo_root, state)
    nxt = _next_question(state)
    if nxt is None:
        return _finalize(repo_root, state)
    _save_state(repo_root, state)
    return _question_payload(nxt, len(state.get("roster", [])))


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
        if q["id"] == "adopt_existing":
            return _answer_adopt_existing(repo_root, state, value)
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

    # define_new_role collects the 8 skeleton fields one at a time
    if q["id"] == "define_new_role":
        return _answer_define_new_role(repo_root, state, value)

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
    adoption_path = _write_adoption(repo_root, state)
    # clear wizard state so a fresh run starts over (re-runnable)
    _state_path(repo_root).unlink(missing_ok=True)
    return {
        "status": "complete",
        "wrote": {
            "setup": str(setup_path),
            "roster": str(roster_path),
            "personas": [str(p) for p in persona_paths],
            "adoption": str(adoption_path) if adoption_path else None,
        },
        "roster_rows": len(roster),
        "adopted_agents": len(state.get("adopted", [])),
        "generated_harness": state.get("generated_harness"),
        "note": "Wizard complete. Every configured value is the operator's; re-run the wizard to change anything.",
    }


def _write_adoption(repo_root: Path, state: dict[str, Any]) -> Path | None:
    """Write the BYOA adoption record (A6) to config/adoption.md."""
    adopted = state.get("adopted", [])
    generated = state.get("generated_harness")
    if not adopted and not generated:
        return None
    p = repo_root / "config" / "adoption.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Adoption (BYOA, A6)",
        "",
        "Agents brought under governance and roles defined through the setup wizard.",
        "",
    ]
    if adopted:
        lines += ["## Adopted agents", "", "| Name | What it does | Role | Instructions |", "|---|---|---|---|"]
        for a in adopted:
            lines.append(f"| {a['name']} | {a['what']} | {a['role'] or '(unmapped)'} | {a['instructions_path'] or '(none)'} |")
        lines.append("")
        # Reconcile results
        for a in adopted:
            if a.get("reconcile"):
                r = a["reconcile"]
                lines += [
                    f"### {a['name']} — reconcile vs {r['role']} harness",
                    "",
                    f"- Covered (dropped, harness carries): {len(r['covered'])}",
                    f"- Compatible (moves into harness/persona): {len(r['compatible'])}",
                    f"- Conflicting (operator decides): {len(r['conflicting'])}",
                    "",
                ]
                if r["conflicting"]:
                    lines += ["Conflicting lines (operator must decide):", ""]
                    for c in r["conflicting"]:
                        lines.append(f"- {c}")
                    lines.append("")
    if generated:
        lines += ["## Generated harness", "", f"- {generated}", ""]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p
