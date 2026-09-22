#!/usr/bin/env python3
"""Collect a reviewable zero-AI evidence bundle after the v2.1 live smoke.

This script never invokes Copilot or any model. It only selects the matching
synthetic smoke session, captures local artifacts, reruns the focused unittest,
and writes a deterministic trace report plus SHA-256 manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import premium_v2_1_trace_report as trace_report  # noqa: E402

SMOKE_SCHEMA = "premium-v2.1-runtime-smoke-fixture-v1"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected top-level JSON object")
    return value


def state_dir_default() -> Path:
    return Path.home() / ".copilot" / "over-the-luna-v2-1" / "state"


def otel_path_from_workspace(workspace: Path) -> Path:
    settings = read_json(workspace / ".vscode" / "settings.json")
    value = settings.get("github.copilot.chat.otel.outfile")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("synthetic workspace does not declare an OTel outfile")
    return Path(value).expanduser().resolve()


def matching_session_keys(state_dir: Path, workspace: Path) -> list[str]:
    matches: list[str] = []
    target = str(workspace.resolve())
    for path in sorted(state_dir.glob("*.events.jsonl")):
        key = path.name[: -len(".events.jsonl")]
        events = trace_report.read_jsonl(path)
        if any(
            isinstance(event.get("cwd"), str)
            and str(Path(event["cwd"]).expanduser().resolve()) == target
            for event in events
            if not event.get("_parse_error")
        ):
            matches.append(key)
    return matches


def run_capture(argv: list[str], *, cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "argv": argv,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def ensure_empty_output(output: Path, workspace: Path) -> None:
    try:
        output.relative_to(workspace)
    except ValueError:
        pass
    else:
        raise ValueError(
            "evidence output must be outside the smoke workspace so collection "
            "cannot invalidate the runtime workspace digest"
        )
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"refusing non-empty evidence output: {output}")
    output.mkdir(parents=True, exist_ok=True)


def copy_if_present(source: Path, destination: Path) -> bool:
    if not source.exists():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return True


def collect(
    workspace: Path,
    *,
    state_dir: Path,
    output: Path,
    session_key: str | None = None,
) -> dict[str, Any]:
    workspace = workspace.expanduser().resolve()
    state_dir = state_dir.expanduser().resolve()
    output = output.expanduser().resolve()

    marker_path = workspace / ".premium-v2-1-smoke.json"
    marker = read_json(marker_path)
    if marker.get("schema") != SMOKE_SCHEMA:
        raise ValueError(
            "refusing evidence collection outside the synthetic v2.1 smoke workspace"
        )

    ensure_empty_output(output, workspace)

    available = matching_session_keys(state_dir, workspace)
    if session_key is None:
        if len(available) != 1:
            raise ValueError(
                "expected exactly one hook session for this workspace; "
                f"found {available!r}. Pass --session-key explicitly."
            )
        selected = available[0]
    else:
        if session_key not in available:
            raise ValueError(
                f"requested session key {session_key!r} does not match workspace; "
                f"available={available!r}"
            )
        selected = session_key

    otel = otel_path_from_workspace(workspace)
    if not otel.exists():
        raise ValueError(f"expected Agent Host OTel file is missing: {otel}")

    raw = output / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    copied: dict[str, str] = {}

    sources = {
        "hook_events": state_dir / f"{selected}.events.jsonl",
        "controller_state": state_dir / f"{selected}.json",
        "controller_proposal": workspace / ".otl-v2-1" / "controller-proposal.json",
        "receipt_index": workspace / ".otl-v2-1" / "receipt-index.json",
        "final_record": workspace / ".otl-v2-1" / "final-record.json",
        "otel": otel,
        "smoke_marker": marker_path,
        "vscode_settings": workspace / ".vscode" / "settings.json",
    }
    for name, source in sources.items():
        suffix = source.suffix or ".txt"
        destination = raw / f"{name}{suffix}"
        if copy_if_present(source, destination):
            copied[name] = str(destination.relative_to(output))

    # Snapshot and adjudicate the runtime state before running any collector-side
    # command that could mutate caches or generated files in the workspace.
    report = trace_report.summarize(
        state_dir,
        workspace,
        None,
        otel,
        selected,
    )
    (output / "trace-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    git = shutil.which("git")
    if git:
        diff = run_capture([git, "diff", "--no-ext-diff"], cwd=workspace)
        status = run_capture([git, "status", "--short"], cwd=workspace)
    else:
        diff = {"argv": ["git", "diff"], "exit_code": None, "stdout": "", "stderr": "git not found"}
        status = {"argv": ["git", "status"], "exit_code": None, "stdout": "", "stderr": "git not found"}
    (output / "git-diff.json").write_text(
        json.dumps(diff, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output / "git-status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    test_result = run_capture(
        [sys.executable, "-m", "unittest", "-v"],
        cwd=workspace,
    )
    (output / "focused-test.json").write_text(
        json.dumps(test_result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    artifact_hashes: dict[str, dict[str, Any]] = {}
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        if path.name == "manifest.json":
            continue
        rel = path.relative_to(output).as_posix()
        artifact_hashes[rel] = {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }

    manifest = {
        "schema": "premium-v2.1-live-smoke-evidence-v1",
        "zero_ai_collection": True,
        "workspace": str(workspace),
        "state_dir": str(state_dir),
        "selected_session_key": selected,
        "matching_session_keys": available,
        "otel_source": str(otel),
        "focused_test_exit": test_result["exit_code"],
        "trace_snapshot_before_collector_test": True,
        "trace_calibration_ready": report["calibration"][
            "ready_for_enforce_mode_candidate"
        ],
        "copied_sources": copied,
        "artifacts": artifact_hashes,
        "limitations": [
            "bundle hashes provide integrity for the collected copy, not same-user tamper resistance before collection",
            "synthetic smoke is runtime calibration only and is not product-quality evidence",
        ],
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, default=state_dir_default())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--session-key")
    args = parser.parse_args(argv)

    try:
        result = collect(
            args.workspace,
            state_dir=args.state_dir,
            output=args.output,
            session_key=args.session_key,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
