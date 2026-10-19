"""No-inference public P5 accounting and adversarial false-proof tests."""
import copy
import json
from pathlib import Path
import unittest
from scripts.role_trace_accounting import account

FIXTURE = Path(__file__).parent / "fixtures" / "p5_role_accounting.json"


class TraceAccountingTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_real_public_p5_accounting(self):
        result = account(self.data)
        base, rc2 = result["arms"]
        self.assertEqual((base["inputTokens"], rc2["inputTokens"]), (44398, 65087))
        self.assertEqual((base["outputTokens"], rc2["outputTokens"]), (1129, 2266))
        self.assertEqual((base["reportedCopilotNanoAiuSum"],
                          rc2["reportedCopilotNanoAiuSum"]), (220272500, 345494500))
        self.assertEqual((base["usageEvents"], rc2["usageEvents"]), (5, 6))
        self.assertEqual(rc2["taskAttempts"], 2)
        self.assertEqual(rc2["roleEvidenceStatus"], "TASK_ATTEMPTS_ONLY")
        self.assertFalse(rc2["hostHandbackProven"])
        self.assertEqual(result["comparison"]["inputTokenDelta"], 20689)
        self.assertEqual(result["comparison"]["inputTokenDeltaPercent"], 46.6)
        self.assertTrue(result["comparison"]["bothQualityAccepted"])
        self.assertFalse(result["comparison"]["councilContributionProven"])

    def test_manufactured_role_chain_flag_cannot_prove_handback(self):
        data = copy.deepcopy(self.data)
        arm = data["arms"][1]
        arm["roleChain"] = True
        arm["architectObserved"] = True
        arm["reviewerObserved"] = True
        self.assertEqual(account(data)["arms"][1]["roleEvidenceStatus"],
                         "TASK_ATTEMPTS_ONLY")

    def test_lifecycle_events_still_do_not_prove_returned_evidence(self):
        data = copy.deepcopy(self.data)
        arm = data["arms"][1]
        arm["subagentStarts"] = [{"name": "Next Architect", "toolCallId": "id1"}]
        arm["subagentCompleted"] = [{"name": "Next Architect", "toolCallId": "id1"}]
        result = account(data)["arms"][1]
        self.assertEqual(result["pairedNamedLifecycleEvents"], 1)
        self.assertEqual(result["roleEvidenceStatus"],
                         "LIFECYCLE_ONLY_HANDOFF_UNVERIFIED")
        self.assertFalse(result["hostHandbackProven"])

    def test_unmatched_lifecycle_id_is_not_counted(self):
        data = copy.deepcopy(self.data)
        arm = data["arms"][1]
        arm["subagentStarts"] = [{"name": "Next Architect", "toolCallId": "id1"}]
        arm["subagentCompleted"] = [{"name": "Next Architect", "toolCallId": "id2"}]
        self.assertEqual(account(data)["arms"][1]["pairedNamedLifecycleEvents"], 0)

    def test_missing_meter_is_unknown_not_zero(self):
        data = copy.deepcopy(self.data)
        data["arms"][1]["usage"][0]["copilotNanoAiu"] = None
        self.assertIsNone(account(data)["arms"][1]["reportedCopilotNanoAiuSum"])

    def test_no_grading_proof_is_not_quality_pass(self):
        data = copy.deepcopy(self.data)
        data["arms"][1]["grading"] = {}
        self.assertFalse(account(data)["arms"][1]["qualityAccepted"])

    def test_invalid_events_are_rejected(self):
        data = copy.deepcopy(self.data)
        data["arms"][0]["events"] = [None]
        with self.assertRaises(ValueError):
            account(data)


if __name__ == "__main__":
    unittest.main()
