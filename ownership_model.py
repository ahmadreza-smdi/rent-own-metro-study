"""Explicit cash-budget scenarios, not actual yields or investment rankings."""
from __future__ import annotations

import math


def payment(principal, annual_rate, years):
    if not all(math.isfinite(v) for v in (principal, annual_rate, years)):
        raise ValueError("Nonfinite loan input")
    if principal < 0 or annual_rate < 0 or years <= 0 or int(years * 12) != years * 12:
        raise ValueError("Invalid loan input")
    n = int(years * 12)
    if principal == 0:
        return 0.0
    r = annual_rate / 12
    if r == 0:
        return principal / n
    return principal * r / -math.expm1(-n * math.log1p(r))


def evaluate(price, gross_monthly_rent, s):
    keys = ("down_payment_fraction", "annual_interest_rate", "loan_years", "occupied_months",
            "management_fraction", "property_tax_fraction", "insurance_fraction",
            "maintenance_reserve_fraction", "monthly_utilities", "monthly_hoa",
            "annual_other_costs", "annual_mortgage_insurance")
    if not all(math.isfinite(s[k]) for k in keys) or not all(math.isfinite(v) for v in (price, gross_monthly_rent)):
        raise ValueError("Nonfinite scenario input")
    if price <= 0 or gross_monthly_rent < 0 or any(s[k] < 0 for k in keys):
        raise ValueError("Negative or missing scenario input")
    if s["down_payment_fraction"] > 1 or s["management_fraction"] >= 1 or s["occupied_months"] > 12:
        raise ValueError("Invalid fraction or occupancy")
    # Gross rent includes a utility allowance. Treat this as an assumed utility
    # deduction before receipts. Never silently floor a negative adjusted rent.
    cash_rent = gross_monthly_rent - s["monthly_utilities"]
    if cash_rent < 0:
        raise ValueError("Utility deduction exceeds gross rent; revise assumptions")
    receipts = cash_rent * s["occupied_months"]
    management = receipts * s["management_fraction"]
    property_tax = price * s["property_tax_fraction"]
    insurance = price * s["insurance_fraction"]
    reserve = price * s["maintenance_reserve_fraction"]
    fixed = property_tax + insurance + reserve + 12 * s["monthly_hoa"] + s["annual_other_costs"] + s["annual_mortgage_insurance"]
    debt = payment(price * (1 - s["down_payment_fraction"]), s["annual_interest_rate"], s["loan_years"]) * 12
    denom = s["occupied_months"] * (1 - s["management_fraction"])
    threshold = s["monthly_utilities"] + (fixed + debt) / denom if denom else None
    surplus = receipts - management - fixed - debt
    return {"annual_receipts": receipts, "annual_management": management,
            "annual_property_tax": property_tax, "annual_insurance": insurance,
            "annual_maintenance_reserve": reserve, "annual_fixed_budget": fixed,
            "annual_principal_interest": debt, "annual_cash_surplus": surplus,
            "break_even_gross_monthly_rent": threshold,
            "input_status": "illustrative"}
