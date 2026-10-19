import unittest
from src.recovery_plan import decide


class RecoveryTests(unittest.TestCase):
    expected = {'title': 'Example task', 'skills': 'Python, SQL'}

    def test_timeout_never_requests_write(self):
        self.assertEqual(decide(self.expected, None, target_matches=True,
                                fresh=False).state, 'RETRY_READ')

    def test_stale_matching_values_not_verified(self):
        self.assertEqual(decide(self.expected, self.expected, target_matches=True,
                                fresh=False, read_attempts=2).state, 'UNVERIFIED')

    def test_only_mismatching_field_then_fresh_verification(self):
        result = decide(self.expected, {'title': 'Example task', 'skills': 'Python'},
                        target_matches=True, fresh=True)
        self.assertEqual((result.state, result.fields), ('REPAIR_FIELDS', ('skills',)))
        self.assertEqual(decide(self.expected, self.expected, target_matches=True,
                                fresh=True, repair_attempts=1).state, 'VERIFIED')

    def test_wrong_target_blocks_even_when_contents_match(self):
        self.assertEqual(decide(self.expected, self.expected, target_matches=False,
                                fresh=True).state, 'BLOCKED_TARGET')

    def test_repair_exhaustion_and_next_independent_task(self):
        self.assertEqual(decide(self.expected, {}, target_matches=True, fresh=True,
                                repair_attempts=1).state, 'INCOMPLETE')
        self.assertEqual(decide(self.expected, self.expected, target_matches=True,
                                fresh=True).state, 'VERIFIED')

    def test_empty_contract_rejected(self):
        with self.assertRaises(ValueError):
            decide({}, {}, target_matches=True, fresh=True)
