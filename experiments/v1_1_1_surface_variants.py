from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

VARIANTS = ("control", "naive", "semantic", "economy")
FINAL_MARKER = "## Final report\n"

NAIVE = """## Surface communication — naive brevity control

Be concise. Keep user-visible progress and the final answer short. Avoid unnecessary detail.

"""

SEMANTIC = """## Surface communication — semantic compression

Reason, investigate, validate, and review as deeply as the task requires. Do not reduce internal work merely to shorten the answer.

Treat user attention as scarce. Preserve only information that can change the user's understanding, decision, trust in the result, or next action.

For user-visible communication:
- lead with the outcome;
- preserve material changes, validation outcomes, actionable Reviewer findings, material caveats, blockers, and required next actions;
- omit request restatement, routine mechanics, repeated evidence, successful intermediate reasoning, and background the user did not ask for;
- compress Architect/Reviewer evidence instead of replaying their reasoning;
- when a Reviewer passes with no actionable finding, one short `Review: PASS` line is sufficient;
- when a finding is accepted and repaired, state the finding, repair, and revalidation once;
- expand when the user explicitly requests detail, when a blocker needs evidence, or when omission would make the result misleading.

"""

ECONOMY = """## Surface communication — attention economy

Reason deeply; communicate economically. Internal reasoning, investigation, validation, and review budgets are unchanged by this section.

User attention is a scarce product resource. Every visible sentence should earn its place by changing the user's understanding, decision, confidence, or next action.

### During work

Required state transitions such as the `Mode:` line and `Boundary sealed — work set:` remain visible exactly as specified. Treat those required markers as the status update; do not surround them with routine narration.

Default to **silent execution between required markers and the final answer**. Tool calls do not need a prose preamble or completion announcement.

Specifically:
- do not send a preparatory message such as “I’ll inspect…”, “I’ll trace…”, or “I’ll implement…” before the route line;
- after the route line, do not narrate successful discovery, reads, edits, test setup, validation setup, diff capture, or Reviewer invocation;
- after a sealed Architect handback, print the required boundary marker and then continue directly with tools;
- do not announce that a patch, tests, diff, or review artifact is “ready” before the next tool call;
- do not announce an action and then separately announce that it completed;
- surface a work-in-progress message only for a blocker/failure that materially changes the plan, a consequential Reviewer finding that requires repair, or a human decision that cannot be taken autonomously;
- when surfacing such an exception, state it once, compactly, and continue without a second recovery-status message unless the state changes again;
- never suppress a required route/boundary marker, a real failure, an unresolved uncertainty, or a consequential Reviewer finding merely to be shorter.

### Final answer

Use progressive disclosure: outcome first; then only material change(s), validation, Reviewer result when used, and non-empty remaining risk or required user action.

Do not restate the request. Do not replay Architect/Reviewer reasoning. Do not list every file or command unless the user asked, a failure requires evidence, or the list itself is the deliverable.

A clean successful coding task should normally fit in one compact paragraph or a few dense bullets. `Review: PASS` is enough for a clean Reviewer pass.

If the user explicitly asks for a detailed explanation, tutorial, audit trail, rationale, or exhaustive evidence, honor that request and expand appropriately. Concision is a default surface policy, not a refusal to provide detail.

"""


def replace_final(text: str, replacement: str) -> str:
    if FINAL_MARKER not in text:
        raise SystemExit("Main agent is missing ## Final report")
    return text.split(FINAL_MARKER, 1)[0] + replacement.rstrip() + "\n"


def build(source: Path, output: Path, variant: str) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copy2(source / "plugin.json", output / "plugin.json")
    shutil.copytree(source / "agents", output / "agents")
    main = output / "agents" / "over-the-luna.agent.md"
    text = main.read_text(encoding="utf-8")

    if variant == "naive":
        text = text.replace(FINAL_MARKER, NAIVE + FINAL_MARKER, 1)
    elif variant == "semantic":
        text = replace_final(text, SEMANTIC + """## Final report

Report the outcome, material change, validation result, Reviewer result when used, and only non-empty remaining risk/human decisions. Preserve required route/assurance semantics but do not turn them into a narrative recap. For NONE, a short note that independent review was intentionally unnecessary is sufficient.
""")
    elif variant == "economy":
        text = replace_final(text, ECONOMY + """## Final report

Default shape for completed implementation work:

`<one-sentence outcome>`

- `Validation: <compact result>`
- `Review: <PASS | concise actionable finding/repaired result>` when review ran
- `Risk/Next: <only if non-empty>`

Mention mode/assurance only when it helps explain a non-obvious route, risk, or user decision; the required route line already recorded it during execution. Preserve material failures and uncertainty even when that makes the answer longer.
""")
    elif variant != "control":
        raise SystemExit(f"unknown variant: {variant}")

    main.write_text(text, encoding="utf-8")
    (output / "variant.json").write_text(json.dumps({"variant": variant}) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--variant", choices=VARIANTS, required=True)
    a = p.parse_args()
    build(a.source.resolve(), a.output.resolve(), a.variant)


if __name__ == "__main__":
    main()
