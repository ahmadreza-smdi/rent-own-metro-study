# Rent and ownership scenarios — Ahmadreza Samadi

Reproducible source for “Where does rent cover the cost of owning?
2026 metro edition.” Results are illustrative cash-budget scenarios, not observed investment returns.

[Open the interactive study](https://a-samadi.com/studies/rent-own-2026/) to inspect the scenarios without installing Python.

## Reproduce offline

Python3.10+ and `openpyxl==3.1.5` are required. The included source files are
public federal outputs with original hashes and URLs in `sources.json`.
No API key, account or private provider dataset is required.

Before the offline steps, install the pinned dependency with
`python3 -m pip install -r requirements.txt`. This setup may need network access;
the reproduction commands below use the included source files offline.

```sh
python3 prepare_sources.py
python3 build_scenarios.py
python3 -m unittest discover -s . -p test_ownership_model.py -v
python3 build_preview.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

Open `http://127.0.0.1:8000/studies/rent-own-2026/`. The rebuilt HTML is deliberately a noindex local preview; the public study
uses the same checked calculation model. All chart computation is
local. Edited assumptions can be downloaded or restored through a URL fragment.
The standalone `embed.html` keeps source years, limits and visible attribution.

`prepare_sources.py` verifies every raw hash, retains all4,764HUD records,
preserves annotations/suppression and compares county membership. The source
population has393metros and142micros; the study retains every available metro.
`build_scenarios.py` creates three labelled hypothetical cases, separate HUD-area
detail and metro min/max scenario ranges. It does not average rent areas or
match owner-stock median values to rental-property purchase prices.

[Read one fictional cash budget step by step](docs/reading-a-budget.md): an illustrated explanation of receipts, costs, reserve and cash surplus. It adds no market observations.

Read `model-method.md` and `data-notes.md` before interpreting any numbers.
Every rate, utility allowance and operating cost is a chosen assumption, not an
observed market value or offer. Surplus is a cash-budget measure after principal
and interest, not accounting profit, actual property yield or total return.
Price/MOE endpoint sensitivity is not a joint confidence interval.

Source vintages: HUD FY2027; ACS2024 one-year B25077; July2023 OMB/Census county
delineation. Edition year2026 is the analysis edition. Known St.Louis statutory
partial-county differences are explicitly labelled; new mismatches stop the build.

## Numeric range validation on main

The main branch rejects calculations whose finite inputs would produce
nonfinite results, and rejects an unrepresentable loan period or a positive
occupancy whose budget denominator underflows to zero. It reports an error
instead of returning infinity or silently treating that occupancy as zero.
Normal fixed study scenarios and their data are unchanged. This validation
is newer than the v1.0.0 release archive; that archive is not replaced.

## Check a repeated rebuild

Run `python3 -B check_rebuild.py` after installing the dependency. It checks the
package manifest, copies the included files into a temporary directory, and
runs source preparation, scenario calculation and preview generation twice.
It compares every generated file's bytes between those two runs without
writing generated outputs into your checkout. GitHub Actions runs this check
and the model tests on Ubuntu with Python 3.10 and 3.13.

With Node.js 18+ available, `python3 -B check_rebuild.py --javascript` also
compares the shipped JavaScript calculation module against all rebuilt Python
metro and HUD-area scenario rows. It checks the fixed scenarios, including
cash purchase, using a USD 0.000001 absolute tolerance for CSV rounding. Missing
or duplicate rows fail the check. GitHub Actions includes this comparison;
it does not run the interactive page in a browser.

This checks repeatability within each runtime, not agreement between runtimes,
browser interaction, geographic equivalence or real investment outcomes.
The manifest detects drift relative to its recorded hashes; it is not a
signature or independent source certification.

## Scenario-link state

After creating a scenario link, changing an assumption, starting case, search
or selected metro hides and clears that old generated link. Create a new link
to share the current inputs and selection. A malformed incoming link still
shows its restoration warning on initial load.

Run `node test_share_state.mjs` with Node.js 18+ for eight scoped UI-state
regressions. They execute the actual UI module with a fictional DOM and model
fixture; they do not certify browser rendering, accessibility or financial
formulas. Both GitHub Actions matrix jobs run these checks. This source fix is
newer than the frozen v1.0.0 archive; the personal website update is separate.

## Files and rights

The package allowlist contains code, method/source notes, citation metadata,
labelled scenarios, aggregate raw inputs, and the Sora font with its original
OFL notice. No account data, credentials, browser receipts, workspace history,
CV, customer records or private company material is included.

Original code is MIT; input datasets and government documents are not relicensed
MIT. HUD/Census policies and third-party exceptions are documented in
`data-notes.md`. Sora retains SIL Open Font License1.1 (`assets/fonts/OFL.txt`).
Agency attribution does not imply endorsement. The manifest records every
included file's hash; it proves bytes, not methodological correctness.

`CITATION.cff` provides version1.0.0 and the public study URL. The repository is
https://github.com/ahmadreza-smdi/rent-own-metro-study. Version 1.0.0 was
[released on 15 October 2026](https://github.com/ahmadreza-smdi/rent-own-metro-study/releases/tag/v1.0.0); no DOI is assigned. See `quarterly-refresh.md`
for the source/coverage/method/release refresh procedure.

Author: [Ahmadreza Samadi](https://a-samadi.com/about.html), Dubai-based technology
entrepreneur. Appraiva first; Royal Abraj Group second as professional background.
