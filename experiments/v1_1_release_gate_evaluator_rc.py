from __future__ import annotations

import sys

import v1_1_release_gate_evaluator_v6 as base

GENERIC_GLOBS = {"*", "**", "**/*", "**/*.*"}


def argument(name: str) -> str | None:
    try:
        index = sys.argv.index(name)
    except ValueError:
        return None
    if index + 1 >= len(sys.argv):
        return None
    return sys.argv[index + 1]


def generic_inventory_failures(case: str, events_path: str) -> list[str]:
    if case not in {"tiny", "local"}:
        return []
    rows = base.load_events(base.Path(events_path))
    failures: list[str] = []
    for row in rows:
        if row.get("type") != "assistant.message" or row.get("agentId"):
            continue
        for request in base.tool_requests(row):
            name = str(request.get("name") or "")
            values = request.get("arguments") or {}
            if name == "apply_patch":
                return failures
            if name == "glob":
                pattern = str(values.get("pattern") or "").strip()
                if pattern in GENERIC_GLOBS:
                    failures.append(f"generic inventory glob is forbidden during local orientation: {pattern}")
    return failures


def main() -> int:
    case = argument("--case")
    events_path = argument("--events")
    base_status = base.main()
    extra: list[str] = []
    if case and events_path:
        extra = generic_inventory_failures(case, events_path)
    for failure in extra:
        print("FAIL:", failure)
    if extra:
        print("RC_EXTRA_GATE: FAIL")
    else:
        print("RC_EXTRA_GATE: PASS")
    return 1 if base_status or extra else 0


if __name__ == "__main__":
    raise SystemExit(main())
