"""Numeric range cases: finite inputs need not yield representable outputs."""
import json
import math
from pathlib import Path
import unittest
from ownership_model import evaluate,payment
BASE=json.loads((Path(__file__).parent/'scenarios.json').read_text())['scenarios'][0]

class NumericRange(unittest.TestCase):
    def test_finite_tax_input_cannot_return_infinite_budget(self):
        with self.assertRaisesRegex(ValueError,'numeric range'):
            evaluate(300000,2000,dict(BASE,property_tax_fraction=1e308))
    def test_receipts_and_debt_overflow_are_errors(self):
        for price,rent,s in [(300000,1e308,BASE),(1e308,2000,dict(BASE,annual_interest_rate=10))]:
            with self.subTest(price=price,rent=rent):
                with self.assertRaisesRegex(ValueError,'numeric range'):evaluate(price,rent,s)
    def test_loan_period_overflow_is_validation_error(self):
        with self.assertRaises(ValueError):payment(1,.06,1e308)
    def test_tiny_positive_occupancy_cannot_become_zero_occupancy(self):
        with self.assertRaisesRegex(ValueError,'numeric range'):
            evaluate(300000,2000,dict(BASE,occupied_months=5e-324,management_fraction=.9))
    def test_zero_occupancy_remains_defined_as_no_threshold(self):
        result=evaluate(300000,2000,dict(BASE,occupied_months=0))
        self.assertIsNone(result['break_even_gross_monthly_rent'])
        self.assertLess(result['annual_cash_surplus'],0)
    def test_large_representable_budget_is_not_arbitrarily_capped(self):
        result=evaluate(1e100,1e90,dict(BASE,down_payment_fraction=1,property_tax_fraction=1e100))
        self.assertTrue(math.isfinite(result['annual_cash_surplus']))
        self.assertLess(result['annual_cash_surplus'],-1e199)

if __name__=='__main__':unittest.main()
