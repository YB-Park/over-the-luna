from __future__ import annotations

import argparse
import sys
import textwrap
import threading
import time
from pathlib import Path

CASES = ("tiny", "broad", "broad_ko", "detail", "risk")


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
        """)
        task = """
            Change the default page size from 50 to 64 and update the exact regression test.
            Preserve explicit page-size overrides and the public function signature. Run the focused/full tests.
            Follow the installed Over the Luna policy naturally. Main remains the only mutation owner.
            Do not use premium review.
        """

    elif case in ("broad", "broad_ko"):
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
        """)
        if case == "broad":
            task = """
                Fix exported account summaries so account identifiers equivalent under the repository's established
                account-ID contract are grouped under the same canonical identity. Preserve order by first canonical
                appearance and reject invalid identifiers exactly like account creation/resource handling. Discover where
                the established identity contract lives rather than duplicating it. Add focused regression tests and run
                the focused/full tests. Follow the installed Over the Luna policy naturally. Main remains the only mutation
                owner. Do not use premium review.
            """
        else:
            task = """
                내보내는 계정 요약에서 저장소의 기존 account-ID 계약상 같은 식별자로 취급되는 값들을 하나의
                canonical identity로 묶어줘. 첫 canonical 등장 순서는 보존하고, 잘못된 식별자는 계정 생성/리소스
                처리와 정확히 같은 방식으로 거부해야 해. 기존 identity 계약이 어디 있는지 먼저 찾아서 재사용하고
                로직을 복제하지 마. 집중 회귀 테스트를 추가하고 관련 테스트와 전체 테스트를 실행해줘.
                설치된 Over the Luna 정책을 자연스럽게 따르고 Main만 파일을 수정해야 해. Premium Review는 쓰지 마.
            """

    elif case == "detail":
        write(root, "routing.py", """
            from dataclasses import dataclass

            @dataclass(frozen=True)
            class Request:
                local: bool
                semantic_change: bool
                high_risk: bool

            def route(req: Request) -> tuple[str, str]:
                if req.high_risk:
                    return ('DEEP' if not req.local else 'SIMPLE', 'RISK')
                if req.local:
                    return ('SIMPLE', 'REVIEW' if req.semantic_change else 'NONE')
                return ('STANDARD', 'REVIEW')
        """)
        task = """
            Do not modify files. Give me a detailed explanation of how routing.py decides investigation mode and
            assurance, including every branch, the precedence between high_risk/local/semantic_change, at least four
            concrete input examples, and any edge cases or ambiguities you notice. I explicitly want detail rather
            than a terse summary. Follow the installed Over the Luna policy naturally and do not use premium review.
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
        """)
        task = """
            Make PaymentService.charge_once linearizable for concurrent retries of the same idempotency key.
            The external charger must be invoked at most once for a successful same-key operation and all concurrent
            callers must observe the same receipt. A charger exception must not poison/cache the key so a later retry
            can succeed. Preserve the public API. This is an idempotency/concurrency correctness boundary. Add focused
            regression tests and run the focused/full tests. Follow the installed Over the Luna policy naturally.
            Main remains the only mutation owner. Do not use premium review.
        """
    else:
        raise SystemExit(case)

    task_file.write_text(textwrap.dedent(task).strip() + "\n", encoding="utf-8")


def hidden(case: str, root: Path) -> None:
    sys.path.insert(0, str(root))
    if case == "tiny":
        from app.config import DEFAULT_PAGE_SIZE, resolve_page_size
        assert DEFAULT_PAGE_SIZE == 64
        assert resolve_page_size() == 64
        assert resolve_page_size(25) == 25
    elif case in ("broad", "broad_ko"):
        from accounts.model import Event
        from accounts.reporting.summary import summarize
        events = [Event('  ACME  ', 2), Event('beta', 4), Event('acme', 3), Event(' BETA ', 1)]
        assert summarize(events) == [('acme', 5), ('beta', 5)]
        try:
            summarize([Event('   ', 1)])
        except ValueError:
            pass
        else:
            raise AssertionError('invalid account id was not rejected')
    elif case == "risk":
        from payments.service import PaymentService

        class SlowCharger:
            def __init__(self):
                self.calls = 0
                self.started = threading.Event()
                self.release = threading.Event()
                self.lock = threading.Lock()
            def charge(self, amount):
                with self.lock:
                    self.calls += 1
                    n = self.calls
                self.started.set()
                self.release.wait(2)
                return f'receipt-{n}-{amount}'

        charger = SlowCharger()
        service = PaymentService(charger)
        results, errors = [], []
        def invoke():
            try:
                results.append(service.charge_once('same', 10))
            except BaseException as exc:
                errors.append(exc)
        t1 = threading.Thread(target=invoke); t1.start()
        assert charger.started.wait(1)
        t2 = threading.Thread(target=invoke); t2.start()
        time.sleep(0.08); charger.release.set(); t1.join(2); t2.join(2)
        assert not errors
        assert charger.calls == 1
        assert len(results) == 2 and results[0] == results[1]

        class Flaky:
            def __init__(self): self.calls = 0
            def charge(self, amount):
                self.calls += 1
                if self.calls == 1: raise RuntimeError('temporary')
                return 'ok'
        flaky = Flaky(); service = PaymentService(flaky)
        try:
            service.charge_once('retry', 5)
        except RuntimeError:
            pass
        else:
            raise AssertionError('expected first failure')
        assert service.charge_once('retry', 5) == 'ok'
        assert flaky.calls == 2
    elif case == "detail":
        return
    else:
        raise SystemExit(case)
    print(f'hidden {case} contract passed')


def main() -> None:
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest='cmd', required=True)
    prep = sub.add_parser('prepare'); prep.add_argument('--case', choices=CASES, required=True); prep.add_argument('--root', type=Path, required=True); prep.add_argument('--task-file', type=Path, required=True)
    hid = sub.add_parser('hidden'); hid.add_argument('--case', choices=CASES, required=True); hid.add_argument('--root', type=Path, required=True)
    a = p.parse_args()
    if a.cmd == 'prepare': prepare(a.case, a.root, a.task_file)
    else: hidden(a.case, a.root)


if __name__ == '__main__':
    main()
