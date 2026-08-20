from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
import threading
import time
from pathlib import Path

CASES = ("tiny", "local", "broad", "risk")


def write(root: Path, path: str, content: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def prepare(case: str, root: Path, task_file: Path) -> None:
    if root.exists():
        raise SystemExit(f"fixture root already exists: {root}")
    root.mkdir(parents=True)

    if case == "tiny":
        write(root, "app/__init__.py", "")
        write(root, "app/config.py", """
            DEFAULT_PAGE_SIZE = 50

            def resolve_page_size(explicit: int | None = None) -> int:
                return DEFAULT_PAGE_SIZE if explicit is None else explicit
        """)
        write(root, "tests/test_config.py", """
            import unittest
            from app.config import resolve_page_size

            class ConfigTests(unittest.TestCase):
                def test_default_page_size(self):
                    self.assertEqual(resolve_page_size(), 50)

                def test_explicit_page_size_is_preserved(self):
                    self.assertEqual(resolve_page_size(25), 25)

            if __name__ == '__main__':
                unittest.main()
        """)
        task = """
            Change the default page size from 50 to 64 and update the exact regression test.
            Preserve explicit page-size overrides and the public function signature. Run the focused/full tests.
            Follow the installed Over the Luna policy naturally. Main remains the only mutation owner.
            Do not use premium review.
        """

    elif case == "local":
        write(root, "client/__init__.py", "")
        write(root, "client/ids.py", """
            def normalize_request_id(value: str) -> str:
                if not isinstance(value, str):
                    raise TypeError('request_id must be a string')
                normalized = value.strip()
                if not normalized:
                    raise ValueError('request_id must not be blank')
                return normalized
        """)
        write(root, "client/headers.py", """
            from .ids import normalize_request_id

            def create_headers(token: str, request_id: str | None = None) -> dict[str, str]:
                headers = {'Authorization': f'Bearer {token}'}
                if request_id is not None:
                    headers['X-Request-ID'] = normalize_request_id(request_id)
                return headers

            def update_headers(token: str, request_id: str | None = None) -> dict[str, str]:
                headers = {'Authorization': f'Bearer {token}'}
                if request_id:
                    headers['X-Request-ID'] = request_id
                return headers
        """)
        write(root, "tests/test_headers.py", """
            import unittest
            from client.headers import create_headers, update_headers

            class HeaderTests(unittest.TestCase):
                def test_create_normalizes_request_id(self):
                    self.assertEqual(create_headers('t', '  abc  ')['X-Request-ID'], 'abc')

                def test_update_without_request_id_preserves_auth(self):
                    self.assertEqual(update_headers('t'), {'Authorization': 'Bearer t'})

            if __name__ == '__main__':
                unittest.main()
        """)
        task = """
            Align update_headers request-ID behavior with the established create_headers contract.
            Explicit non-None IDs must use the shared normalization/validation behavior; blank IDs must be rejected;
            absence must still omit X-Request-ID; Authorization behavior must not change. Add focused regression tests
            and run the focused/full tests. Follow the installed Over the Luna policy naturally. Main remains the only
            mutation owner. Do not use premium review.
        """

    elif case == "broad":
        write(root, "accounts/__init__.py", "")
        write(root, "accounts/core/__init__.py", "")
        write(root, "accounts/core/identity.py", """
            def normalize_account_id(raw: str) -> str:
                if not isinstance(raw, str):
                    raise TypeError('account_id must be a string')
                value = raw.strip().lower()
                if not value:
                    raise ValueError('account_id must not be blank')
                return value
        """)
        write(root, "accounts/api.py", """
            from .core.identity import normalize_account_id

            def account_resource(account_id: str) -> str:
                return f'/accounts/{normalize_account_id(account_id)}'
        """)
        write(root, "accounts/model.py", """
            from dataclasses import dataclass

            @dataclass(frozen=True)
            class Event:
                account_id: str
                amount: int
        """)
        write(root, "accounts/storage.py", """
            from .model import Event

            def load_rows(rows: list[tuple[str, int]]) -> list[Event]:
                return [Event(account_id, amount) for account_id, amount in rows]
        """)
        write(root, "accounts/reporting/__init__.py", "")
        write(root, "accounts/reporting/summary.py", """
            from collections import OrderedDict
            from ..model import Event

            def summarize(events: list[Event]) -> list[tuple[str, int]]:
                totals: OrderedDict[str, int] = OrderedDict()
                for event in events:
                    totals[event.account_id] = totals.get(event.account_id, 0) + event.amount
                return list(totals.items())
        """)
        write(root, "tests/test_accounts.py", """
            import unittest
            from accounts.api import account_resource
            from accounts.model import Event
            from accounts.reporting.summary import summarize

            class AccountTests(unittest.TestCase):
                def test_resource_uses_canonical_identity(self):
                    self.assertEqual(account_resource('  ACME  '), '/accounts/acme')

                def test_summary_preserves_first_seen_order(self):
                    events = [Event('a', 1), Event('b', 2), Event('a', 3)]
                    self.assertEqual(summarize(events), [('a', 4), ('b', 2)])

            if __name__ == '__main__':
                unittest.main()
        """)
        task = """
            Fix exported account summaries so account identifiers equivalent under the repository's established
            account-ID contract are grouped under the same canonical identity. Preserve order by first canonical
            appearance and reject invalid identifiers exactly like account creation/resource handling. Discover where
            the established identity contract lives rather than duplicating it. Add focused regression tests and run
            the focused/full tests. Follow the installed Over the Luna policy naturally. Main remains the only mutation
            owner. Do not use premium review.
        """

    elif case == "risk":
        write(root, "payments/__init__.py", "")
        write(root, "payments/service.py", """
            class PaymentService:
                def __init__(self, charger):
                    self._charger = charger
                    self._receipts: dict[str, object] = {}

                def charge_once(self, idempotency_key: str, amount: int):
                    existing = self._receipts.get(idempotency_key)
                    if existing is not None:
                        return existing
                    receipt = self._charger.charge(amount)
                    self._receipts[idempotency_key] = receipt
                    return receipt
        """)
        write(root, "tests/test_service.py", """
            import unittest
            from payments.service import PaymentService

            class Charger:
                def __init__(self):
                    self.calls = 0
                def charge(self, amount):
                    self.calls += 1
                    return f'receipt-{self.calls}-{amount}'

            class PaymentTests(unittest.TestCase):
                def test_sequential_retry_is_idempotent(self):
                    charger = Charger()
                    service = PaymentService(charger)
                    first = service.charge_once('k', 10)
                    second = service.charge_once('k', 10)
                    self.assertEqual(first, second)
                    self.assertEqual(charger.calls, 1)

                def test_distinct_keys_charge_independently(self):
                    charger = Charger()
                    service = PaymentService(charger)
                    service.charge_once('a', 10)
                    service.charge_once('b', 10)
                    self.assertEqual(charger.calls, 2)

            if __name__ == '__main__':
                unittest.main()
        """)
        task = """
            Make PaymentService.charge_once linearizable for concurrent retries of the same idempotency key.
            The external charger must be invoked at most once for a successful same-key operation and all concurrent
            callers must observe the same receipt. A charger exception must not poison/cache the key so a later retry
            can succeed. Preserve distinct-key and public API behavior. This is an idempotency/concurrency correctness
            boundary. Add focused regression tests and run the focused/full tests. Follow the installed Over the Luna
            policy naturally. Main remains the only mutation owner. Do not use premium review.
        """
    else:
        raise SystemExit(f"unknown case: {case}")

    task_file.write_text(textwrap.dedent(task).strip() + "\n", encoding="utf-8")


def run_hidden(case: str, root: Path) -> None:
    sys.path.insert(0, str(root))
    if case == "tiny":
        from app.config import DEFAULT_PAGE_SIZE, resolve_page_size
        assert DEFAULT_PAGE_SIZE == 64
        assert resolve_page_size() == 64
        assert resolve_page_size(25) == 25

    elif case == "local":
        from client.headers import update_headers
        assert update_headers("t", "  abc  ") == {
            "Authorization": "Bearer t", "X-Request-ID": "abc"
        }
        assert update_headers("t") == {"Authorization": "Bearer t"}
        for bad in ("", "   "):
            try:
                update_headers("t", bad)
            except ValueError:
                pass
            else:
                raise AssertionError("blank request id was not rejected")

    elif case == "broad":
        from accounts.model import Event
        from accounts.reporting.summary import summarize
        events = [Event("  ACME  ", 2), Event("beta", 4), Event("acme", 3), Event(" BETA ", 1)]
        assert summarize(events) == [("acme", 5), ("beta", 5)]
        try:
            summarize([Event("   ", 1)])
        except ValueError:
            pass
        else:
            raise AssertionError("invalid account id was not rejected")

    elif case == "risk":
        from payments.service import PaymentService

        class SlowCharger:
            def __init__(self) -> None:
                self.calls = 0
                self.started = threading.Event()
                self.release = threading.Event()
                self._lock = threading.Lock()

            def charge(self, amount: int) -> str:
                with self._lock:
                    self.calls += 1
                    call_no = self.calls
                self.started.set()
                self.release.wait(2)
                return f"receipt-{call_no}-{amount}"

        charger = SlowCharger()
        service = PaymentService(charger)
        results: list[object] = []
        errors: list[BaseException] = []

        def invoke() -> None:
            try:
                results.append(service.charge_once("same", 10))
            except BaseException as exc:
                errors.append(exc)

        t1 = threading.Thread(target=invoke)
        t1.start()
        assert charger.started.wait(1), "first charge never started"
        t2 = threading.Thread(target=invoke)
        t2.start()
        time.sleep(0.08)
        charger.release.set()
        t1.join(2)
        t2.join(2)
        assert not t1.is_alive() and not t2.is_alive(), "concurrent calls deadlocked"
        assert not errors, errors
        assert charger.calls == 1, charger.calls
        assert len(results) == 2 and results[0] == results[1], results

        class FlakyCharger:
            def __init__(self) -> None:
                self.calls = 0

            def charge(self, amount: int) -> str:
                self.calls += 1
                if self.calls == 1:
                    raise RuntimeError("temporary failure")
                return "ok"

        flaky = FlakyCharger()
        service = PaymentService(flaky)
        try:
            service.charge_once("retry", 5)
        except RuntimeError:
            pass
        else:
            raise AssertionError("expected first failure")
        assert service.charge_once("retry", 5) == "ok"
        assert flaky.calls == 2
    else:
        raise SystemExit(f"unknown case: {case}")

    print(f"hidden {case} contract passed")


def load_events(path: Path) -> list[dict]:
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def task_requests(message: dict) -> list[dict]:
    data = message.get("data") or {}
    requests = data.get("toolRequests") or []
    return [r for r in requests if isinstance(r, dict)]


def parse_route(events: list[dict]) -> tuple[str | None, str | None]:
    route_re = re.compile(r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)", re.S)
    for event in events:
        if event.get("type") != "assistant.message" or event.get("agentId"):
            continue
        content = str((event.get("data") or {}).get("content") or "")
        match = route_re.search(content)
        if match:
            return match.group(1), match.group(2)
    return None, None


def evaluate(case: str, events_path: Path, ownership_path: Path) -> int:
    events = load_events(events_path)
    ownership = json.loads(ownership_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    mode, assurance = parse_route(events)
    expected_mode, expected_assurance = {
        "tiny": ("SIMPLE", "NONE"),
        "local": ("SIMPLE", "REVIEW"),
        "broad": ("STANDARD", "REVIEW"),
        "risk": (None, "RISK"),
    }[case]
    if expected_mode is not None and mode != expected_mode:
        failures.append(f"route mode expected {expected_mode}, got {mode}")
    if assurance != expected_assurance:
        failures.append(f"assurance expected {expected_assurance}, got {assurance}")

    subagent_names = [
        str((event.get("data") or {}).get("agentName") or "")
        for event in events
        if event.get("type") == "subagent.started"
    ]
    reviewer_count = sum(name.endswith("luna-reviewer") for name in subagent_names)
    architect_count = sum(name.endswith("luna-architect") for name in subagent_names)
    premium_count = sum("sonnet" in name.lower() or "opus" in name.lower() for name in subagent_names)

    expected_reviewer = {"tiny": 0, "local": 1, "broad": 1}.get(case)
    if expected_reviewer is not None and reviewer_count != expected_reviewer:
        failures.append(f"Reviewer count expected {expected_reviewer}, got {reviewer_count}")
    if case == "risk" and not (1 <= reviewer_count <= 2):
        failures.append(f"RISK Reviewer count expected 1..2, got {reviewer_count}")
    expected_architect = {"tiny": 0, "local": 0, "broad": 1}.get(case)
    if expected_architect is not None and architect_count != expected_architect:
        failures.append(f"Architect count expected {expected_architect}, got {architect_count}")
    if premium_count:
        failures.append(f"automatic premium subagent count must be 0, got {premium_count}")

    by_agent = ownership.get("by_agent") or {}
    for agent, tools in by_agent.items():
        if agent.endswith("luna-reviewer"):
            reads = sum(int(tools.get(name, 0)) for name in ("view", "rg", "glob", "search", "read"))
            if reads > 8:
                failures.append(f"Reviewer read/search budget exceeded: {reads} > 8")
        if agent != "over-the-luna:over-the-luna":
            for mutation_tool in ("apply_patch", "edit", "create", "delete"):
                if int(tools.get(mutation_tool, 0)):
                    failures.append(f"leaf agent {agent} used mutation tool {mutation_tool}")

    reviewer_task_prompts: list[str] = []
    architect_completed_index: int | None = None
    for index, event in enumerate(events):
        if event.get("type") == "subagent.completed":
            name = str((event.get("data") or {}).get("agentName") or "")
            if name.endswith("luna-architect"):
                architect_completed_index = index
        if event.get("type") == "assistant.message" and not event.get("agentId"):
            for request in task_requests(event):
                if request.get("name") != "task":
                    continue
                args = request.get("arguments") or {}
                if str(args.get("agent_type") or "").endswith("luna-reviewer"):
                    reviewer_task_prompts.append(str(args.get("prompt") or ""))

    for prompt in reviewer_task_prompts:
        has_concrete_diff = (
            "diff --git" in prompt
            or "```diff" in prompt
            or ("Current diff" in prompt and "@@" in prompt)
        )
        if not has_concrete_diff:
            failures.append("Reviewer prompt missing concrete diff/hunk artifact")

    for event in events:
        if event.get("type") != "assistant.message" or not event.get("agentId"):
            continue
        for request in task_requests(event):
            if request.get("name") == "view":
                path = str((request.get("arguments") or {}).get("path") or "")
                if "/.git" in path or path.endswith("/.git"):
                    failures.append(f"Reviewer/leaf attempted .git inspection: {path}")

    if case == "broad" and architect_completed_index is not None:
        shell_broad = re.compile(r"(^|[;&|]\s*)(find\s+\.|ls\s+-R|tree(?:\s|$)|git\s+(?:grep|ls-files)|grep\s+-R|rg(?:\s|$))")
        for event in events[architect_completed_index + 1:]:
            if event.get("type") != "assistant.message" or event.get("agentId"):
                continue
            for request in task_requests(event):
                name = str(request.get("name") or "")
                args = request.get("arguments") or {}
                if name in {"rg", "glob"}:
                    failures.append(f"Main replayed broad discovery after Architect via {name}")
                elif name == "view":
                    path = str(args.get("path") or "")
                    if path and not Path(path).suffix and not path.endswith(".agent.md"):
                        failures.append(f"Main viewed directory after Architect handback: {path}")
                elif name == "bash":
                    command = str(args.get("command") or "")
                    if shell_broad.search(command):
                        failures.append(f"Main used shell broad discovery after Architect: {command[:160]}")

    print("POLICY_GATE:", "PASS" if not failures else "FAIL")
    print(f"- route={mode}+{assurance}")
    print(f"- architect={architect_count}")
    print(f"- reviewer={reviewer_count}")
    print(f"- premium={premium_count}")
    for failure in failures:
        print("FAIL:", failure)
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare")
    p_prepare.add_argument("--case", choices=CASES, required=True)
    p_prepare.add_argument("--root", type=Path, required=True)
    p_prepare.add_argument("--task-file", type=Path, required=True)

    p_hidden = sub.add_parser("hidden")
    p_hidden.add_argument("--case", choices=CASES, required=True)
    p_hidden.add_argument("--root", type=Path, required=True)

    p_eval = sub.add_parser("evaluate")
    p_eval.add_argument("--case", choices=CASES, required=True)
    p_eval.add_argument("--events", type=Path, required=True)
    p_eval.add_argument("--ownership", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.case, args.root, args.task_file)
        return 0
    if args.command == "hidden":
        run_hidden(args.case, args.root)
        return 0
    return evaluate(args.case, args.events, args.ownership)


if __name__ == "__main__":
    raise SystemExit(main())
