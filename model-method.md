# Cash-budget scenario method — private calculation stage

## What decision does this change?

An AI summary may quote one rent and one value for a metro. This study makes the
next check explicit: would the rent cover the selected annual cash budget, and
does the answer change across HUD rent areas inside the metro? It does not match
a rental property's price to its rent or rank places to invest.

The intended public title remains “Where does rent cover the cost of owning?
2026 metro edition.” Its subtitle must state “Illustrative cash budgets using
HUD FY2027 two-bedroom gross rents and ACS 2024 owner-stock values.”

## Geographic treatment

Retain all 393 metros in the available ACS one-year population. Within each
metro, retain **all distinct HUD areas** identified by the documented CBSA prefix
and county coverage check. Confirm identical bedroom rents across repeated
county/town rows of each HUD area; contradictions stop the build. Never weight
by county count, population or pretend rental inventory.

For each metro, use the minimum and maximum calculated cash surplus across those
HUD area rents. Expandable detail must name every HUD area and preserve its code.
The endpoints are subarea scenarios, not observed lowest/highest rents, an
average, a probability interval or assurance that any particular property exists.

County membership agrees in 392 metros. St. Louis is retained with its specific
HUD statutory Sullivan City/Crawford County exception visibly labelled; no
general allowance for future county mismatches exists. New missing/extra county
sets stop the model. Equal county sets do not establish town-level identity.
The range uses the HUD-defined area's published rent without claiming its exact
boundaries equal the Census metro.

## Inputs and formulas

`scenarios.json` holds three explicitly hypothetical cases: financed, cash and
higher-cost. Rates, tax/insurance/reserve fractions, occupancy, utility allowance,
management and HOA are **chosen assumptions**, not federal observations,
regional averages, actual quotes or predictions. The public interactive chart
must expose editable inputs and the selected assumptions beside its results.

- Price proxy P = ACS median value of all owner-occupied housing units.
- Gross monthly rent G = selected HUD two-bedroom FMR.
- Monthly utility assumption U is deducted from gross rent before landlord cash
  receipts; vacancy applies once to those adjusted receipts.
- Occupied months O is between zero and twelve; receipts R = (G − U) × O.
- Management cash cost = R × management fraction m.
- Fixed annual budget F = P × (tax + insurance + maintenance-reserve fractions)
  + twelve HOA payments + other annual costs + mortgage insurance assumption.
- Loan principal L = P × (1 − down-payment fraction). Fixed monthly principal
  and interest uses Lr / (1 − (1+r)^−n), with monthly interest r and n monthly
  payments. At zero rate, payment = L/n; cash purchase has zero loan payments.
- Annual debt payment D = twelve principal-and-interest payments. Taxes and
  insurance are counted in F once; D contains **no escrow**.
- Annual cash surplus = R × (1−m) − F − D.
- Break-even gross monthly rent = U + (F + D) / [O × (1−m)]. At zero occupancy,
  the threshold is undefined, not zero. Reject utility assumptions above G,
  invalid fractions, nonfinite inputs and negative costs.

Maintenance is an earmarked cash reserve in this budget; it is not claimed to
be a realized annual expense. Do not add the same capital expenditure again.
The mortgage payment includes principal: surplus is a cash-budget figure, not
accounting profit, net operating income or total investment return.

## Sensitivity and exclusions

Recompute at P minus and plus the ACS published margin of error, holding chosen
cost fractions constant. Those endpoints illustrate the price-proxy effect;
they are **not a joint confidence interval** for rent, cost or surplus. Carry
the original estimate and MOE in both detail and download. Unsupported/missing
estimates remain unresolved; no imputation or zero filling is allowed.

The three cases show assumption sensitivity, not optimism/base/downside
probabilities. Even the cash case can have a cash surplus while offering poor
total return. This model excludes acquisition/sale costs, initial repairs,
down-payment opportunity cost, appreciation, income tax, depreciation benefits,
refinancing, rent growth and future capital surprises. Zero HOA/other/mortgage
insurance is a **scenario assumption**, not evidence that those costs are absent.
Actual costs and property-specific prices/rents must replace proxies before a
personal transaction decision. No personalized investment advice is generated.

## Primary sources for payment interpretation

[CFPB mortgage payment components](https://www.consumerfinance.gov/ask-cfpb/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment-en-1941/)
supports separating principal/interest from taxes, insurance and other charges.
[CFPB amortization explanation](https://www.consumerfinance.gov/ask-cfpb/how-does-paying-down-a-mortgage-work-en-1943/)
supports distinguishing principal repayment from interest and equity. Both were
opened on 15 October 2026. The numerical scenario inputs are project assumptions.
