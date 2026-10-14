"""Build a private static preview; no public checkout edits or network calls."""
import csv
import argparse
import hashlib
import html
import json
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parents[1] / "a-samadi.com" / "ahmadreza-smdi.github.io"

def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main(font_path=None):
    receipt = json.loads((ROOT / "preparation.json").read_text())
    for name, spec in receipt["outputs"].items():
        if hashlib.sha256((ROOT / "prepared" / name).read_bytes()).hexdigest() != spec["sha256"]:
            raise ValueError("Prepared input changed; rebuild sources")
    groups = defaultdict(dict)
    for h in read(ROOT / "prepared" / "hud-records.csv"):
        groups[h["candidate_cbsa"]][h["hud_area_code"]] = {
            "code": h["hud_area_code"], "name": h["hud_area_name"], "rent": float(h["fmr_2"])}
    metros=[]
    for m in read(ROOT / "prepared" / "cbsa-candidates.csv"):
        if m["area_kind"] != "metro": continue
        metros.append({"cbsa":m["cbsa"],"name":m["name"],"price":float(m["median_owner_value_usd"]),
                       "moe":float(m["moe_usd"]),"exception":bool(m["extra_counties"]),
                       "areas":list(groups[m["cbsa"]].values())})
    metros.sort(key=lambda m:m["name"])
    fields=[
        ("down_payment_fraction","Down payment (%)",True,100),
        ("annual_interest_rate","Fixed annual interest (%)",True,None),
        ("loan_years","Loan term (years)",False,None),
        ("occupied_months","Paid months per year",False,12),
        ("management_fraction","Management (% of receipts)",True,99.99),
        ("property_tax_fraction","Annual property tax (% of value)",True,None),
        ("insurance_fraction","Annual insurance (% of value)",True,None),
        ("maintenance_reserve_fraction","Annual maintenance reserve (% of value)",True,None),
        ("monthly_utilities","Monthly utility deduction (USD)",False,None),
        ("monthly_hoa","Monthly HOA (USD)",False,None),
        ("annual_other_costs","Other annual costs (USD)",False,None),
        ("annual_mortgage_insurance","Annual mortgage insurance (USD)",False,None)]
    data={"metros":metros,"scenarios":json.loads((ROOT/"scenarios.json").read_text())["scenarios"],
          "fields":[{"key":k,"label":l,"percent":p,**({"max":maxv} if maxv is not None else {})} for k,l,p,maxv in fields]}
    out=ROOT/"web"/"studies"/"rent-own-2026";out.mkdir(parents=True,exist_ok=True)
    font=ROOT/"web"/"assets"/"fonts";font.mkdir(parents=True,exist_ok=True)
    selected_font=Path(font_path) if font_path else ROOT/"assets/fonts/sora-latin-wght.woff2"
    if not selected_font.exists(): selected_font=SITE/"assets/fonts/sora-latin-wght.woff2"
    shutil.copyfile(selected_font,font/"sora-latin-wght.woff2")
    for filename in ("study-model.mjs","study-ui.mjs","study.css"):
        shutil.copyfile(ROOT/filename,out/filename)
    cases={s["id"]:s for s in data["scenarios"]}
    assumption_keys=[f["key"] for f in data["fields"]]
    for filename in ("metro-scenarios.csv","hud-area-scenarios.csv"):
        rows=read(ROOT/"model"/filename)
        for row in rows:
            row.update({key:cases[row["scenario"]][key] for key in assumption_keys})
        with (out/filename).open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (out/"study-data.json").write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    data_inline=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    url="https://a-samadi.com/studies/rent-own-2026/"
    snippet=f'<iframe src="{url}embed.html" title="Rent and ownership cash-budget scenarios by Ahmadreza Samadi" width="100%" height="1100" loading="lazy"></iframe>\n<p>Source: <a href="{url}">Ahmadreza Samadi — rent and ownership scenarios</a>. HUD FY2027 / ACS 2024; illustrative assumptions.</p>'
    schema={"@context":"https://schema.org","@type":"WebApplication","name":"Rent and ownership cash-budget scenarios",
            "applicationCategory":"FinanceApplication","operatingSystem":"Any web browser","isAccessibleForFree":True,
            "author":{"@type":"Person","name":"Ahmadreza Samadi","url":"https://a-samadi.com/about.html"},"url":url}
    template='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rent and ownership scenarios | Ahmadreza Samadi</title><meta name="robots" content="noindex,nofollow"><meta name="author" content="Ahmadreza Samadi">
<meta name="description" content="Explore hypothetical ownership cash budgets across US metros using HUD rent areas and ACS owner-stock values. Methods and limitations are explicit.">
<link rel="canonical" href="__URL__"><link rel="stylesheet" href="study.css?v=20261015-study1"><script type="module" src="study-ui.mjs?v=20261015-study1"></script>
<script type="application/ld+json">__SCHEMA__</script></head><body class="__BODY__"><header><a href="https://a-samadi.com/">Ahmadreza Samadi</a> · Start with the decision</header><main>
<div class="full-only"><p class="eyebrow">Private preview · 2026 metro edition</p><h1>Where does rent cover the cost of owning?</h1>
<p class="lead">Illustrative cash budgets using HUD FY2027 two-bedroom gross rents and ACS 2024 owner-stock values. Explore every metro in the available one-year Census universe and the different HUD rent areas inside it.</p></div>
<p class="note">These are scenarios, not observed investment returns. Rent and value describe different housing populations. Every rate and operating cost below is a chosen assumption; replace it with property-specific evidence before making a decision.</p>
<section class="panel" aria-labelledby="assumption-title"><h2 id="assumption-title">Which assumptions change the answer?</h2><label>Starting case<select id="preset"></select></label><p class="small">Cash purchase assumes no loan. Zero costs in a case are assumptions, not evidence of absence. Edited inputs remain in this browser; the chart sends no inputs to a server.</p><div id="assumptions"></div><dl id="print-assumptions"></dl><p id="error" role="alert"></p></section>
<section class="panel" aria-labelledby="chart-title"><h2 id="chart-title">Compare cash-budget ranges</h2><div class="controls"><label>Find a metro or CBSA code<input id="search" type="search" placeholder="For example: St. Louis"></label><label>Order<select id="sort"><option value="name">Alphabetical</option><option value="surplus">Lowest scenario surplus first</option></select></label></div><p id="count" role="status"></p><p id="axis" class="small"></p>
<div class="table-wrap"><table><caption>Annual surplus across distinct HUD rent areas; select a metro for detail.</caption><thead><tr><th scope="col">Metro</th><th scope="col">HUD areas</th><th scope="col">Range around zero</th><th scope="col">Annual cash surplus (USD)</th></tr></thead><tbody id="result-body"></tbody></table></div>
<div class="actions pager"><button id="previous">Previous</button><span id="page"></span><button id="next">Next</button></div><div class="actions"><button id="download-current">Download this scenario CSV</button><button id="print">Print / save PDF</button><button id="share">Create scenario link</button></div>
<label class="full-only share-only">Scenario link<input id="share-url" type="text" readonly hidden></label><p id="share-status" class="small" role="status"></p><p class="small">Current-scenario download includes every filtered metro, all assumption values and unresolved inputs. Print includes every filtered row, beyond the current screen page.</p><noscript><p>The interactive chart needs JavaScript. <a href="metro-scenarios.csv">Download all three fixed scenarios</a> and <a href="hud-area-scenarios.csv">HUD-area detail</a>.</p></noscript></section>
<section id="detail" class="panel" aria-labelledby="selected-name"><h2 id="selected-name"></h2><p id="selected-proxy"></p><p id="threshold"></p><div class="table-wrap"><table><caption>Every candidate HUD area for the selected metro; no geographic average.</caption><thead><tr><th scope="col">HUD area</th><th scope="col">Source code</th><th scope="col">Two-bedroom gross rent/month</th><th scope="col">Scenario surplus/year</th></tr></thead><tbody id="area-body"></tbody></table></div><p id="budget" class="small"></p></section>
<section class="panel full-only"><h2>What does this calculation include?</h2><p>Cash receipts = (HUD gross rent − chosen monthly utilities) × paid months. Management is deducted from those receipts. The annual budget includes chosen property tax, insurance, maintenance reserve, HOA, other costs and mortgage insurance, plus loan principal and interest. Taxes and insurance are counted once; the loan payment excludes escrow.</p><p>Break-even gross monthly rent = utilities + (fixed annual budget + annual principal/interest) ÷ [paid months × (1 − management fraction)]. At zero paid months, that threshold is undefined. A negative surplus stays negative; incomplete or invalid inputs are never replaced with zero.</p>
<h2>Why show a range?</h2><p>A Census metro can contain multiple HUD rent areas. We retain every distinct area, instead of averaging or selecting the central one. The chart's endpoints are their calculated scenarios, not the lowest/highest observed rents. The same metro owner-stock value proxy is used for each area; it is not a matched rental-property price.</p><p>The owner-value margin of error is retained. Price-minus-MOE and price-plus-MOE sensitivity endpoints are shown in detail and downloads; they are not a confidence interval for cash surplus. County membership agrees in 392 metros. St. Louis retains HUD's statutory Sullivan City/Crawford County exception. County agreement does not certify town-level equivalence.</p>
<h2>What remains outside the budget?</h2><p>Acquisition and sale costs, initial repairs, down-payment opportunity cost, appreciation, income tax, depreciation benefits, refinancing, rent growth and future capital surprises. Maintenance is an earmarked reserve, not a realized annual expense. Principal repayment affects cash and equity; surplus is not accounting profit or total return.</p>
<h2>Sources and downloads</h2><ul><li><a href="https://www.huduser.gov/portal/datasets/fmr.html">HUD Fair Market Rents — FY2027</a></li><li><a href="https://www.huduser.gov/portal/datasets/fmr/fmr2027/FY27-Public-FMR-Methodology.pdf">HUD methodology — June 2026, geography pages 1–4</a></li><li><a href="https://www.census.gov/programs-surveys/acs/data/summary-file.html">Census ACS 2024 one-year B25077 — owner value and margin of error</a></li><li><a href="https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html">July 2023 county delineation</a></li><li><a href="https://www.consumerfinance.gov/ask-cfpb/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment-en-1941/">CFPB payment components</a></li><li><a href="metro-scenarios.csv">All three fixed scenarios CSV</a> · <a href="hud-area-scenarios.csv">All HUD-area details CSV</a></li></ul><p class="small">Federal output reuse follows the agencies' published policies, with third-party exceptions retained. Original code is MIT; input data is not relicensed MIT. Agency names indicate sources, not endorsement. Reproducible repository and citation metadata are prepared but not publicly released. The planned 29 October 2026 ACS 2025 release will be checked before the final study release.</p>
<p class="small"><a href="https://www.hud.gov/sites/documents/webpubstandards.pdf">HUD reuse policy, section 1D</a> · <a href="https://www2.census.gov/foia/ds_policies/ds027.pdf">Census public-access policy</a>.</p><h2>Use the next decision check</h2><p><a href="https://a-samadi.com/writing/ai-rental-yield-cash-flow.html">Rental yield versus cash flow</a> · <a href="https://a-samadi.com/watch/rental-yield.html">The rental-yield film</a> · <a href="https://a-samadi.com/tools/rental-cash-flow.html">Property-specific cash-flow calculator</a></p>
<div class="embed-instructions"><h2>Embed with attribution</h2><p>The embed preserves the source years, assumptions and Ahmadreza Samadi attribution. This snippet is prepared for the future public release; the destination is not live yet.</p><label>Embed HTML<textarea readonly>__SNIPPET__</textarea></label></div></section>
<p class="attribution">Study and original code by <a href="https://a-samadi.com/about.html">Ahmadreza Samadi</a> · <a href="__URL__">Full method and study</a>. Sources: HUD FY2027 / ACS 2024. Illustrative cash budgets, not investment returns.</p></main><footer>Ahmadreza Samadi · Dubai-based technology entrepreneur. Appraiva, Co-Founder &amp; Technical Lead (Cleveland, Ohio; remote); Royal Abraj Group, Co-Founder &amp; CEO. <a href="https://www.linkedin.com/newsletters/7516204575893393408/">Get the weekly brief</a>.</footer><script id="study-data" type="application/json">__DATA__</script></body></html>'''
    for name,body in (("index.html",""),("embed.html","embed-only")):
        content=template.replace('__URL__',url).replace('__SCHEMA__',json.dumps(schema)).replace('__DATA__',data_inline).replace('__SNIPPET__',html.escape(snippet)).replace('__BODY__',body)
        (out/name).write_text(content)
    print(f'Private preview built: {out}; {len(metros)} metros')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-path',help='Existing Sora font file; bundled font is used when present')
    main(parser.parse_args().font_path)
