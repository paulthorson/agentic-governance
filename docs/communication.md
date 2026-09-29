# Communication Rules

Free communication between fifty autonomous bots is not collaboration. Work gets reframed at every hop, nobody owns the original problem, and tokens burn on bots agreeing with each other.

**Directed edges only:**

- PM receives from CEO bot, hands to UX
- UX receives from PM, hands to engineer
- Engineer receives from UX, hands to QA
- QA receives from UX and engineer, reports up to CEO bot
- Cross-team traffic routes through CEO bots

**Chief of Staff edge (multi-team mode).** When the operator runs more than
one project or team at once, Cos receives from CEO bots only; producing roles
do not message Cos. In multi-team mode, CEO → human becomes CEO → Cos → human.
Cross-CEO disagreement still reaches the human, but packaged by Cos.
Single-team mode unchanged: CEO → human.

**Review edge.** The adversarial agents review CEO rulings per Section 12 of the framework. This is the only path by which a decision moves back down the chain.

**One exception.** The adversarial agents get read access across everything. Judging requires seeing raw work rather than a summary of it, which is consistent with the existing rule that raw adversary transcripts are committed before any executive summary.

_Content per Section 6 of `agent-harnesses.md` (ratified)._
