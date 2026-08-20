from __future__ import annotations

import sys
from pathlib import Path

import v1_1_release_gate_evaluator_v6 as base

BACKGROUND_NAMES = {
    "README",
    "README.md",
    "README.rst",
    "CHANGELOG",
    "CHANGELOG.md",
    "CONTRIBUTING",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE.md",
}


def argument(name: str) -> str | None:
    try:
        index = sys.argv.index(name)
    except ValueError:
        return None
    return sys.argv[index + 1] if index + 1 < len(sys.argv) else None


def extra_failures(case: str, events_path: str) -> list[str]:
    if case not in {"tiny", "local"}:
        return []

    rows = base.load_events(Path(events_path))
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
                failures.append("glob is forbidden during SIMPLE local orientation; use exact rg/direct reads")
            elif name == "view":
                path = base.normalize(str(values.get("path") or ""))
                candidate = Path(path)
                if candidate.name in BACKGROUND_NAMES or "docs" in candidate.parts:
                    failures.append(f"background prose is forbidden during local orientation: {path}")
    return failures


def main() -> int:
    case = argument("--case")
    events_path = argument("--events")
    base_status = base.main()
    failures: list[str] = []
    if case and events_path:
        failures = extra_failures(case, events_path)
    for failure in failures:
        print("FAIL:", failure)
    print("RC2_EXTRA_GATE:", "PASS" if not failures else "FAIL")
    return 1 if base_status or failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
