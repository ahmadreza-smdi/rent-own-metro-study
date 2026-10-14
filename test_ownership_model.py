"""Independent arithmetic, boundary and sensitivity checks for the cash model."""
import json
import math
import unittest
from pathlib import Path

from ownership_model import evaluate, payment

BASE = json.loads((Path(__file__).parent / "scenarios.json").read_text())["scenarios"][0]


class OwnershipTests(unittest.TestCase):
    def test_amortization_pays_balance_without_escrow(self):
        # Independently iterate the balance rather than repeat the payment formula.
        principal = 200000
        monthly = payment(principal, .06, 30)
        self.assertAlmostEqual(monthly, 1199.1010503055, places=8)
        balance = principal
        for _ in range(360):
            balance = balance * (1 + .06 / 12) - monthly
        self.assertAlmostEqual(balance, 0, places=6)

    def test_zero_rate_cash_and_invalid_loan(self):
        self.assertEqual(payment(12000, 0, 1), 1000)
        self.assertEqual(payment(0, .08, 30), 0)
        for args in ((1, -.01, 30), (1, .01, 0), (-1, .01, 30), (math.inf, .01, 30)):
            with self.assertRaises(ValueError):
                payment(*args)

    def test_hand_calculated_budget_and_no_tax_double_count(self):
        s = dict(BASE, down_payment_fraction=1, occupied_months=10, management_fraction=.1,
                 monthly_utilities=100, property_tax_fraction=.01, insurance_fraction=.005,
                 maintenance_reserve_fraction=.01, monthly_hoa=25, annual_other_costs=200)
        # (1000-100)*10=9000; fee900; tax1000+ins500+reserve1000+HOA300+other200=3000.
        r = evaluate(100000, 1000, s)
        self.assertEqual(r["annual_receipts"], 9000)
        self.assertEqual(r["annual_fixed_budget"], 3000)
        self.assertEqual(r["annual_principal_interest"], 0)
        self.assertEqual(r["annual_cash_surplus"], 5100)

    def test_break_even_round_trip_and_rent_slope(self):
        r = evaluate(300000, 2000, BASE)
        boundary = r["break_even_gross_monthly_rent"]
        self.assertAlmostEqual(evaluate(300000, boundary, BASE)["annual_cash_surplus"], 0, places=7)
        difference = evaluate(300000, 2100, BASE)["annual_cash_surplus"] - r["annual_cash_surplus"]
        self.assertAlmostEqual(difference, 100 * 11 * .92, places=7)

    def test_sensitivity_direction_and_zero_occupancy(self):
        lo = evaluate(290000, 2000, BASE)["annual_cash_surplus"]
        hi = evaluate(310000, 2000, BASE)["annual_cash_surplus"]
        self.assertGreater(lo, hi)
        self.assertLess(evaluate(300000, 2000, dict(BASE, annual_interest_rate=.08))["annual_cash_surplus"], evaluate(300000, 2000, BASE)["annual_cash_surplus"])
        r = evaluate(300000, 2000, dict(BASE, occupied_months=0))
        self.assertEqual(r["annual_receipts"], 0)
        self.assertIsNone(r["break_even_gross_monthly_rent"])

    def test_invalid_scenarios_do_not_become_zero_or_negative_fees(self):
        for change in ({"management_fraction":1}, {"occupied_months":13}, {"down_payment_fraction":1.1}, {"monthly_utilities":3000}, {"insurance_fraction":float('nan')}):
            with self.assertRaises(ValueError):
                evaluate(300000, 2000, dict(BASE, **change))


if __name__ == "__main__":
    unittest.main()
