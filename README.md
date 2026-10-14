# Rent and ownership scenarios — Ahmadreza Samadi

Reproducible source for “Where does rent cover the cost of owning?
2026 metro edition.” Results are illustrative cash-budget scenarios, not observed investment returns.

## Reproduce offline

Python3.10+ and `openpyxl==3.1.5` are required. The included source files are
public federal outputs with original hashes and URLs in `sources.json`.
No API key, account or private provider dataset is required.

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

Read `model-method.md` and `data-notes.md` before interpreting any numbers.
Every rate, utility allowance and operating cost is a chosen assumption, not an
observed market value or offer. Surplus is a cash-budget measure after principal
and interest, not accounting profit, actual property yield or total return.
Price/MOE endpoint sensitivity is not a joint confidence interval.

Source vintages: HUD FY2027; ACS2024 one-year B25077; July2023 OMB/Census county
delineation. Edition year2026 is the analysis edition. Known St.Louis statutory
partial-county differences are explicitly labelled; new mismatches stop the build.

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
https://github.com/ahmadreza-smdi/rent-own-metro-study. Add a release date or DOI
only when it actually exists. See `quarterly-refresh.md`
for the source/coverage/method/release refresh procedure.

Author: [Ahmadreza Samadi](https://a-samadi.com/about.html), Dubai-based technology
entrepreneur. Appraiva first; Royal Abraj Group second as professional background.
