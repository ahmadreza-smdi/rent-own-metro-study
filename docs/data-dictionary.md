# Scenario data dictionary

The two CSV files in `model/` describe hypothetical cash budgets built from
the included sources and assumptions. `metro-scenarios.csv` summarizes the
range across candidate HUD rent areas. `hud-area-scenarios.csv` retains each
candidate area separately. Neither file measures a property's investment return.

The fixed build produces 1,179 metro/scenario rows with 18 columns and 1,947
HUD-area/scenario rows with 21 columns. Use `(scenario, cbsa)` as the summary
key and `(scenario, cbsa, hud_area_code)` as the detail key. Keep identifiers as
text, including leading zeros. All money is in US dollars.

The definitions below follow [the CSV builder](../build_scenarios.py) and
[the budget model](../ownership_model.py). For source populations, geographic
exceptions and reuse terms, read [data notes](../data-notes.md) and
[the model method](../model-method.md). This guide describes the repository's
current rebuild; it does not replace the frozen v1.0.0 release archive.

## Fields shared by both files

| Field | Type or unit | Meaning |
| --- | --- | --- |
| `scenario` | Text | Assumption-set ID in `scenarios.json`: `illustrative-financed`, `illustrative-cash` or `illustrative-stress`. |
| `cbsa` | Five-character text | Census metropolitan-area identifier used for candidate matching. It is not a HUD rent-area identifier. |
| `metro` | Text | Metropolitan-area name retained from source preparation. |
| `hud_fiscal_year` | Integer year | HUD FMR fiscal year, 2027 in this source edition. It is distinct from the ACS observation year. |
| `acs_year` | Integer year | ACS one-year owner-value observation year, 2024 in this source edition. |
| `owner_value_proxy_usd` | USD | ACS B25077 median value for owner-occupied units, used as the scenario price proxy. It is not the purchase price of a matched two-bedroom rental property. |
| `owner_value_moe_usd` | USD | Published margin of error for that owner-value estimate. The model also evaluates price minus/plus this amount as sensitivity endpoints. |

## Metro summary fields

These 11 fields, together with the seven shared fields, make the 18-column
`metro-scenarios.csv`. A minimum and maximum summarize candidate subareas;
the builder does not calculate a geographic average rent.

| Field | Type or unit | Meaning |
| --- | --- | --- |
| `hud_area_count` | Integer count | Number of distinct candidate HUD rent areas evaluated for the metro. |
| `hud_2br_gross_min_usd` | USD per month | Lowest two-bedroom gross FMR among those candidate areas. |
| `hud_2br_gross_max_usd` | USD per month | Highest two-bedroom gross FMR among those candidate areas. |
| `cash_surplus_min_usd` | USD per year | Lowest modeled annual cash surplus across candidate rents at the central owner-value proxy. |
| `cash_surplus_max_usd` | USD per year | Highest modeled annual cash surplus across candidate rents at the central owner-value proxy. |
| `price_endpoint_surplus_min_usd` | USD per year | Lowest surplus across candidate rents and the central, minus-MOE and plus-MOE price calculations. |
| `price_endpoint_surplus_max_usd` | USD per year | Highest surplus across those same calculations. These endpoints are not a joint confidence interval. |
| `break_even_gross_monthly_usd` | USD per month | Gross monthly rent needed for zero annual cash surplus at the central price proxy and chosen assumptions. This threshold is the same across candidate rents within that metro/scenario. |
| `scenario_coverage` | Text category | Whether all, some or none of the candidate-rent budgets have nonnegative annual cash surplus; see the exact categories below. |
| `geography_note` | Text category | County-set comparison or the retained St. Louis partial-county exception. Equal county sets do not prove identical town/subcounty boundaries or housing populations. |
| `interpretation` | Text | Scope label: illustrative cash budget, not an investment return or recommendation. |

`scenario_coverage` uses these boundaries:

- `all_candidate_rents_cover`: the minimum annual surplus is at least zero.
- `some_candidate_rents_cover`: the minimum is below zero and the maximum is
  at least zero.
- `no_candidate_rent_covers`: the maximum is below zero.

The geography labels are `county_sets_equal; HUDsubareas_preserved` and
`statutory_partial_county_exception`. The second preserves the documented
St. Louis exception rather than changing county membership to force a match.

## HUD area detail fields

These 14 fields, together with the seven shared fields, make the 21-column
`hud-area-scenarios.csv`. The owner-value proxy stays at metro level while
rent varies by candidate HUD area.

| Field | Type or unit | Meaning |
| --- | --- | --- |
| `hud_area_code` | Text | Complete HUD rent-area identifier. Preserve the full code rather than only its CBSA-like prefix. |
| `hud_area_name` | Text | HUD area name retained from the source workbook. |
| `hud_2br_gross_monthly_usd` | USD per month | Source two-bedroom gross FMR used for this candidate area. The model deducts the assumed monthly utility amount before calculating landlord receipts. |
| `annual_receipts` | USD per year | `(gross monthly rent − monthly utilities) × occupied months`. Occupancy and utilities are chosen assumptions. |
| `annual_management` | USD per year | Annual receipts multiplied by the assumed management fraction. |
| `annual_property_tax` | USD per year | Price proxy multiplied by the assumed annual property-tax fraction. |
| `annual_insurance` | USD per year | Price proxy multiplied by the assumed annual insurance fraction. |
| `annual_maintenance_reserve` | USD per year | Price proxy multiplied by the assumed reserve fraction. This is a budgeted set-aside, not an observed maintenance bill. |
| `annual_fixed_budget` | USD per year | Tax, insurance and reserve, plus 12 times monthly HOA and the assumed annual other costs and mortgage insurance. It excludes management and principal/interest. |
| `annual_principal_interest` | USD per year | Twelve monthly amortizing loan payments, including principal and interest. It is zero for the fixed cash-purchase case. |
| `annual_cash_surplus` | USD per year | Receipts minus management, fixed budget and principal/interest. A negative value is a modeled annual shortfall. |
| `break_even_gross_monthly_rent` | USD per month | The detail-file name for the central-price break-even threshold. The fixed cases use positive occupancy and produce a numeric threshold. |
| `input_status` | Text | `illustrative`: the financing, occupancy and operating inputs are scenarios. |
| `interpretation` | Text | Reminder that HUD-subarea rent is combined with a metro owner-stock value proxy, without matching a particular property. |

## Assumptions and precision

Read the chosen row in [scenarios.json](../scenarios.json) with any output.
Fractions use decimal notation: `0.08` means 8 percent. The loan term is in
years, occupancy is in months per year, and utilities/HOA are monthly amounts.
Other costs and mortgage insurance are annual amounts. These are teaching
assumptions, not quoted rates, assessed taxes, lending offers or forecasts.

The CSV builder rounds calculated floating-point model outputs to six decimal
places. That formatting supports reproducible comparisons; it does not imply
that the source estimates or hypothetical budgets are known to six-decimal
accuracy. Retain negative signs and source years when quoting a result.

## Rebuild and cite

After installing the dependency in `requirements.txt`, run the commands from
the repository root:

```sh
python3 prepare_sources.py
python3 build_scenarios.py
```

This creates the source intermediates and both model CSVs. For the full
repeatability and JavaScript-parity checks, follow [the README](../README.md).
Use [CITATION.cff](../CITATION.cff) for the released software citation. When
citing a current-main change, also identify the commit and keep the scenario,
HUD fiscal year, ACS year and interpretation limits with the quoted figure.

By [Ahmadreza Samadi](https://a-samadi.com/about.html), as part of
Property Decision Data.
