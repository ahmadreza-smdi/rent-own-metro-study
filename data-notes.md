# Sources, reuse and interpretation

Prepared 15 October 2026. This is a source/method record, not legal certification,
investment advice, a public result or native/human review evidence.

## Source vintages and units

- **HUD FY2027 FMR**: monthly US dollars, bedroom-specific, county/town records
  assigned to HUD rent areas. The workbook dictionary identifies FY2027.
  [Official FMR index](https://www.huduser.gov/portal/datasets/fmr.html).
- **ACS 2024 one-year B25077**: median value of owner-occupied housing units and
  its margin of error. Preserve the estimate/MOE and original annotation fields.
  These are housing-stock statistics, not a purchase-price quote for a matching
  two-bedroom rental property. [Summary files](https://www.census.gov/programs-surveys/acs/data/summary-file.html).
- **July 2023 OMB delineation**, distributed by Census: county/equivalent members
  of CBSAs. [Official delineation page](https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html).
- **Upcoming ACS**: Census's schedule, updated 13 October 2026, plans the 2025
  one-year release for **29 October 2026**. Do not treat it as already available
  or guarantee the date. Recheck that page for the next refresh.
  [Release schedule](https://www.census.gov/programs-surveys/acs/news/data-releases/2025/release-schedule.html).

The title's “2026 edition” is the analysis edition, not a claim that every input
was observed in 2026. Display HUD fiscal year and ACS observation year prominently.

## Rent and geographic meaning

The downloaded HUD methodology has **23 PDF pages**, headed “Updated June 2026”.
Page 1 describes a 40th-percentile recent-mover estimate; pages 1–3 explain areas
and HUD subareas; page 4 describes the Sullivan City exception and ACS standard-
quality gross-rent input. Gross rent includes utility treatment; landlord cash
receipts must not be equated to that gross figure without explicit assumptions.
[Official methodology](https://www.huduser.gov/portal/datasets/fmr/fmr2027/FY27-Public-FMR-Methodology.pdf).

HUD area-code constructs 2, 3, 5 and 6 can identify separate HUD areas within
the same OMB metro (page 3 footnote 5). Parsing a CBSA prefix is candidate mapping,
not geographic equivalence. A metro can have multiple materially different FMRs.
Do not select only the central HUD area or average by county count/population
and present that as an observed rent. A range can preserve subarea uncertainty,
but needs a documented coverage method and exception treatment first.

Even correct boundaries do not make the housing populations comparable. Combining
a two-bedroom FMR with all-owner-unit median value is an illustrative screening
scenario, not property yield, profitability, appraisal or a buy/sell recommendation.

## Reuse record

The plan requests US federal sources. Census's downloaded public-access policy
DS027 distinguishes employee-created works from contractor/third-party material
and notes that copyright treatment outside the US may differ. Keep source
attribution and the original policy; do not assert blanket worldwide CC0.
[Census policy PDF](https://www2.census.gov/foia/ds_policies/ds027.pdf).

The inputs here are public agency outputs, not downloads of the proprietary
providers that contribute to HUD's estimation process. HUD's opened **27 August
2025 Web Publication Procedures and Style Guide**, page 1 section 1D, establishes
its general public-domain treatment with identified outside-source exceptions.
The value-bearing FMR workbook cells and its dictionary contain no copyright or
licence notice in the recorded scan. This is the reuse basis for the public HUD
output, not a newly granted licence or a worldwide CC0 declaration.
[HUD policy](https://www.hud.gov/sites/documents/webpubstandards.pdf).

The PDF was read through the web tool; a separate raw download returned 403 and
was not retried or bypassed. Earlier guessed policy pages failed and remain
irrelevant to the actual basis. `method-sources.json` records the opened policy,
its scope and the bounded notice scan. Retain agency attribution and applicable
third-party notices; do not imply HUD/Census endorsement. No new account, API
key, terms acceptance, private dataset or permission change was used.

The MIT licence in this directory applies **only to original project code**.
It does not license the raw government files, third-party material, source PDFs,
or portraits. `CITATION.cff` identifies software version1.0.0 and the study URL; its repository
URL is verified; release dates/DOIs must be added only when they actually exist.
