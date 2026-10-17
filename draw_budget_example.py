"""Render an explicitly fictional cash budget; optional Matplotlib dependency."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt'] = 'fictional-cash-budget'
import matplotlib.pyplot as plt
from ownership_model import evaluate

ROOT = Path(__file__).resolve().parent
# Reuse the hand-calculated cash-purchase case in test_ownership_model.py.
s = dict(json.loads((ROOT / 'scenarios.json').read_text())['scenarios'][0],
         id="fictional-cash-budget-example", label="Fictional cash-purchase budget example",
         down_payment_fraction=1, occupied_months=10, management_fraction=.1,
         monthly_utilities=100, property_tax_fraction=.01, insurance_fraction=.005,
         maintenance_reserve_fraction=.01, monthly_hoa=25, annual_other_costs=200)
r = evaluate(100000, 1000, s)
assert (r['annual_receipts'], r['annual_management'], r['annual_fixed_budget'],
        r['annual_principal_interest'], r['annual_cash_surplus']) == (9000, 900, 3000, 0, 5100)
out = ROOT / 'docs'; out.mkdir(exist_ok=True)
fig, ax = plt.subplots(figsize=(12, 7.2), dpi=150)
fig.patch.set_facecolor('#f5faf8'); ax.set_facecolor('#f5faf8')
labels = ['Rent cash\nreceipts', 'Management', 'Chosen fixed\nbudget + reserve', 'Loan principal\nand interest', 'Cash surplus']
changes = [9000, -900, -3000, 0, 5100]
bottoms = [0, 8100, 5100, 5100, 0]
heights = [9000, 900, 3000, 0, 5100]
colors = ['#639d94', '#c0d6df', '#c0d6df', '#c0d6df', '#2d6965']
for i, (bottom, height, color, change) in enumerate(zip(bottoms, heights, colors, changes)):
    ax.bar(i, height, bottom=bottom, width=.65, color=color, zorder=3)
    if not height: ax.plot([i-.32,i+.32], [bottom,bottom], color='#55747b', lw=3, zorder=4)
    ax.text(i, bottom+height+220, ('−' if change<0 else '')+f'${abs(change):,}', ha='center', fontsize=13, fontweight='bold', color='#193e45')
    if i<3: ax.plot([i+.325,i+.675], [bottom,bottom] if i else [9000,9000], color='#99b0b2', ls='--', lw=1)
ax.set_xticks(range(5), labels, fontsize=11)
ax.set_ylim(0,10500); ax.set_yticks([0,3000,6000,9000], ['$0','$3,000','$6,000','$9,000'])
ax.tick_params(axis='both', length=0, labelcolor='#193e45'); ax.grid(axis='y', color='#dce7e5', zorder=0)
for spine in ax.spines.values(): spine.set_visible(False)
fig.text(.09,.94,'Rent receipts are not cash surplus',fontsize=23,fontweight='bold',color='#193e45')
fig.text(.09,.89,'FICTIONAL CASH-PURCHASE EXAMPLE · USD PER YEAR',fontsize=11,color='#385e63')
fig.text(.09,.16,'Receipts: ($1,000 gross rent − $100 utilities) × 10 paid months = $9,000.',fontsize=11,color='#193e45')
fig.text(.09,.115,'Fixed budget: $1,000 tax + $500 insurance + $1,000 reserve + $300 HOA + $200 other.',fontsize=10.5,color='#193e45')
fig.text(.09,.065,'Chosen assumptions; no real property or market result. Surplus is not profit or investment return.',fontsize=10,color='#193e45')
fig.text(.09,.025,'Ahmadreza Samadi · Educational, not financial advice.',fontsize=10,color='#385e63')
fig.subplots_adjust(left=.09,right=.97,top=.83,bottom=.26)
fig.savefig(out/'budget-example-FICTIONAL.png',dpi=150)
fig.savefig(out/'budget-example-FICTIONAL.svg',metadata={'Date':None})
plt.close(fig)
alt='Fictional cash-purchase budget, in annual USD: rent cash receipts 9,000, less management 900, less fixed budget including reserve 3,000, less loan principal and interest zero, leaves cash surplus 5,100. Receipts equal (1,000 gross monthly rent minus 100 utilities) times 10 paid months. A chosen 100,000 price supports the tax, insurance and reserve assumptions; it is not a real property price. Fixed budget is tax 1,000, insurance 500, maintenance reserve 1,000, HOA 300 and other costs 200. Cash surplus is not profit or investment return. By Ahmadreza Samadi; educational, not financial advice.'
(out/'budget-example-FICTIONAL.alt.txt').write_text(alt+'\n')
(out/'budget-example-FICTIONAL.json').write_text(json.dumps({'kind':'fictional_teaching_example','source_case':'test_ownership_model.py:test_hand_calculated_budget_and_no_tax_double_count','price_assumption_usd':100000,'gross_monthly_rent_assumption_usd':1000,'assumptions':s,'model_outputs':r,'matplotlib_version':matplotlib.__version__,'actual_market_observation':False},indent=2)+'\n')
