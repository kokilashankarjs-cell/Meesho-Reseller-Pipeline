import unittest
from growth_engine import mom_growth, is_flagged, validate_feed


class TestGrowthEngine(unittest.TestCase):

    def test_ethnic_wear_growth(self):
        result = mom_growth(104520.77, 185107.61)
        self.assertEqual(result, 77.1)
        self.assertEqual(is_flagged(result), "flagged")

    def test_beauty_growth(self):
        result = mom_growth(35542.11, 37559.07)
        self.assertEqual(result, 5.67)
        self.assertEqual(is_flagged(result), "not_flagged")

    def test_exact_boundary(self):
        result = mom_growth(100000, 108000)
        self.assertEqual(result, 8.0)
        self.assertEqual(is_flagged(result), "escalate_exact_boundary")

    def test_corrupted_feed(self):
        valid, errors = validate_feed(
            r"fixtures\corrupted_feed.csv"
        )

        self.assertFalse(valid)

        expected_errors = [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)",
        ]

        self.assertEqual(errors, expected_errors)


if __name__ == "__main__":
    unittest.main()