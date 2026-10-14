"""Build all-metro scenario ranges without averaging HUD subareas."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from ownership_model import evaluate

ROOT = Path(__file__).resolve().parent


def read(name):
    with (ROOT / "prepared" / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    receipt = json.loads((ROOT / "preparation.json").read_text())
    for name, info in receipt["outputs"].items():
        if hashlib.sha256((ROOT / "prepared" / name).read_bytes()).hexdigest() != info["sha256"]:
            raise ValueError(f"Prepared input changed: {name}; rerun source preparation")
    scenarios = json.loads((ROOT / "scenarios.json").read_text())["scenarios"]
    by_cbsa = defaultdict(dict)
    for row in read("hud-records.csv"):
        key = row["hud_area_code"]
        existing = by_cbsa[row["candidate_cbsa"]].get(key)
        if existing and any(existing[f"fmr_{n}"] != row[f"fmr_{n}"] for n in range(5)):
            raise ValueError(f"Conflicting rents within HUD area {key}")
        by_cbsa[row["candidate_cbsa"]][key] = row
    metros = [m for m in read("cbsa-candidates.csv") if m["area_kind"] == "metro"]
    outputs, details = [], []
    for m in metros:
        # A known statutory partial-county exception is retained explicitly.
        # No general exemption is permitted for a newly mismatching metro.
        if m["missing_counties"] or (m["extra_counties"] and not (m["cbsa"] == "41180" and m["extra_counties"] == "29056")):
            raise ValueError(f"Unresolved new county mismatch: {m['cbsa']}")
        if m["estimate_status"] != "numeric" or m["moe_status"] != "numeric":
            raise ValueError(f"Missing owner-value estimate/MOE: {m['cbsa']}")
        price, moe = float(m["median_owner_value_usd"]), float(m["moe_usd"])
        if price - moe <= 0:
            raise ValueError("Nonpositive value sensitivity endpoint")
        areas = by_cbsa[m["cbsa"]]
        if not areas:
            raise ValueError("No HUD candidate area")
        for s in scenarios:
            evaluated = []
            for code, h in sorted(areas.items()):
                rent = float(h["fmr_2"])
                base = evaluate(price, rent, s)
                low_price = evaluate(price - moe, rent, s)
                high_price = evaluate(price + moe, rent, s)
                evaluated.append((base, low_price, high_price))
                details.append({"scenario": s["id"], "cbsa": m["cbsa"], "metro": m["name"],
                                "hud_area_code": code, "hud_area_name": h["hud_area_name"],
                                "hud_fiscal_year": 2027, "acs_year": 2024, "hud_2br_gross_monthly_usd": rent,
                                "owner_value_proxy_usd": price, "owner_value_moe_usd": moe,
                                **{k: round(v, 6) if isinstance(v, float) else v for k, v in base.items()},
                                "interpretation": "HUD-subarea rent with metro owner-stock value proxy; not matched property"})
            base_results = [r[0] for r in evaluated]
            endpoints = [r for triple in evaluated for r in triple]
            bottom = min(r["annual_cash_surplus"] for r in base_results)
            top = max(r["annual_cash_surplus"] for r in base_results)
            outputs.append({"scenario": s["id"], "cbsa": m["cbsa"], "metro": m["name"],
                            "hud_fiscal_year": 2027, "acs_year": 2024, "hud_area_count": len(areas),
                            "owner_value_proxy_usd": price, "owner_value_moe_usd": moe,
                            "hud_2br_gross_min_usd": min(float(h["fmr_2"]) for h in areas.values()),
                            "hud_2br_gross_max_usd": max(float(h["fmr_2"]) for h in areas.values()),
                            "cash_surplus_min_usd": round(bottom, 6), "cash_surplus_max_usd": round(top, 6),
                            "price_endpoint_surplus_min_usd": round(min(r["annual_cash_surplus"] for r in endpoints), 6),
                            "price_endpoint_surplus_max_usd": round(max(r["annual_cash_surplus"] for r in endpoints), 6),
                            "break_even_gross_monthly_usd": round(base_results[0]["break_even_gross_monthly_rent"], 6),
                            "scenario_coverage": "all_candidate_rents_cover" if bottom >= 0 else "some_candidate_rents_cover" if top >= 0 else "no_candidate_rent_covers",
                            "geography_note": "statutory_partial_county_exception" if m["extra_counties"] else "county_sets_equal; HUDsubareas_preserved",
                            "interpretation": "illustrative cash budget, not investment return or recommendation"})
    target = ROOT / "model"
    target.mkdir(exist_ok=True)
    for name, rows in (("metro-scenarios.csv", outputs), ("hud-area-scenarios.csv", details)):
        with (target / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary = {"status": "private calculated scenarios; not published or investment results",
               "metro_count": len(metros), "scenario_count": len(scenarios), "metro_scenario_rows": len(outputs),
               "hud_area_scenario_rows": len(details), "input_assumptions_sha256": hashlib.sha256((ROOT / "scenarios.json").read_bytes()).hexdigest(),
               "geographic_average_used": False, "moe_endpoints_are_joint_confidence_interval": False,
               "outputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.glob("*.csv"))}}
    (target / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
