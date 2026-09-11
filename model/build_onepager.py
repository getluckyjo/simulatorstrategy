"""One-page financial analysis of the Virgin Active bay opportunity, from model.json."""
import json, base64
d = json.load(open("model.json")); B = d["cases"]["base"]; Lc = d["cases"]["low"]; Hc = d["cases"]["high"]; U = d["unit"]
font = base64.b64encode(open("../golfzon/fonts/PosterGothicRoundATF-Heavy.woff2", "rb").read()).decode()
Y = list(range(2027, 2033)); R = lambda C, y: C["rows"][str(y)]
m = lambda x, dp=0: ("−" if x < 0 else "") + f"R{abs(x)/1e6:.{dp}f}m"
k = lambda x: f"R{x/1e3:,.0f}k"
pct = lambda x: f"{x*100:.0f}%"
def irr(cfs):
    lo, hi = -0.99, 10
    for _ in range(200):
        mid = (lo + hi) / 2
        if sum(cf / (1 + mid) ** i for i, cf in enumerate(cfs)) > 0: lo = mid
        else: hi = mid
    return mid
proj = [R(B, y)["ebitda"] - R(B, y)["capex"] for Y_ in [Y] for y in Y_]
proj_irr = irr(proj)
cum_ebitda = sum(R(B, y)["ebitda"] for y in Y); cum_va = sum(R(B, y)["va_share"] for y in Y); cum_ds = sum(R(B, y)["debt_service"] for y in Y)
eq = lambda C: -min(R(C, y)["cum_cash"] for y in Y)
cum_cash = lambda C: R(C, 2032)["cum_cash"]
rev31 = R(B, 2031); mix = {"Bay hire": rev31["bay_hire"], "Golf add-on": rev31["membership"], "Insured shot": rev31["challenge"], "Leagues and events": rev31["leagues"], "Naming partner": rev31["sponsorship"]}
# payback year of total capex from cumulative EBITDA
acc = 0; payback = None
for y in Y:
    acc += R(B, y)["ebitda"]
    if acc >= B["total_capex"] and payback is None: payback = y
# break-evens
import importlib.util
spec = importlib.util.spec_from_file_location("mm", "model.py"); mm = importlib.util.module_from_spec(spec); spec.loader.exec_module(mm)
def be(target):
    lo, hi = 0.1, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if mm.run(mid)["rows"][2031]["dscr"] < target: lo = mid
        else: hi = mid
    r = mm.run(mid)["rows"][2031]; return r["hours"] / 200 / 360, r["revenue"]
be10 = be(1.0); be13 = be(1.3)

def unit_tbl():
    rows = [("Landed and installed", lambda u: k(u["capex"])), ("Booked hours a day", lambda u: f"{u['hours']/360:.1f}"), ("Revenue", lambda u: k(u["revenue"])), ("To Virgin Active, 20%", lambda u: k(u["va_share"])), ("EBITDA", lambda u: f"<b>{k(u['ebitda'])}</b>"), ("Margin", lambda u: pct(u["margin"])), ("RMB instalments", lambda u: k(u["debt_service"])), ("Cash after debt", lambda u: f"<b>{k(u['cash_after_debt'])}</b>"), ("Payback from EBITDA", lambda u: f"{u['payback_years']:.1f} yrs")]
    h = "<table><tr><th>A bay at maturity</th><th>Signature</th><th>Play</th><th>Practice</th></tr>"
    for lab, f in rows: h += f"<tr><td>{lab}</td>" + "".join(f"<td>{f(U[t])}</td>" for t in ("Signature", "Play", "Practice")) + "</tr>"
    return h + "</table>"
def chain_tbl():
    rows = [("Bays live", lambda r: f"{r['bays']}"), ("Revenue", lambda r: m(r["revenue"])), ("To Virgin Active", lambda r: m(r["va_share"])), ("EBITDA", lambda r: f"<b>{m(r['ebitda'])}</b>"), ("RMB interest and capital", lambda r: m(r["debt_service"])), ("Debt cover", lambda r: f"{r['dscr']:.1f}×"), ("Cumulative cash, after deposits", lambda r: m(r["cum_cash"]))]
    h = "<table><tr><th>Base case</th>" + "".join(f"<th>{y}</th>" for y in Y) + "</tr>"
    for lab, f in rows: h += f"<tr><td>{lab}</td>" + "".join(f"<td>{f(R(B, y))}</td>" for y in Y) + "</tr>"
    return h + "</table>"
def cases_tbl():
    rows = [("Booked hours a bay a day", lambda C: f"{R(C,2031)['hours']/200/360:.1f}"), ("Revenue 2031", lambda C: m(R(C, 2031)["revenue"])), ("EBITDA 2031", lambda C: m(R(C, 2031)["ebitda"])), ("Debt cover 2031", lambda C: f"{R(C,2031)['dscr']:.1f}×"), ("Equity needed", lambda C: f"<b>{m(eq(C))}</b>"), ("Cash after debt and deposits, 2027–32", lambda C: m(cum_cash(C)))]
    h = "<table><tr><th>Three cases</th><th>Low</th><th>Base</th><th>High</th></tr>"
    for lab, f in rows: h += f"<tr><td>{lab}</td>" + "".join(f"<td>{f(C)}</td>" for C in (Lc, B, Hc)) + "</tr>"
    return h + "</table>"
def mix_tbl():
    tot = sum(mix.values())
    h = "<table><tr><th>Revenue mix, 2031</th><th>Rm</th><th>Share</th></tr>"
    for lab, v in mix.items(): h += f"<tr><td>{lab}</td><td>{m(v)}</td><td>{pct(v/tot)}</td></tr>"
    return h + "</table>"

page = f"""<title>Virgin Active Bay Economics</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>
@font-face {{ font-family: "PosterGothic"; src: url(data:font/woff2;base64,{font}) format("woff2"); font-weight: 800; }}
:root {{ --bg:#f5f0e1; --paper:#fdfcf5; --ink:#16261a; --ink2:#3d4a3f; --mute:#6b746c; --line:#d6ccb2; --green:#335231; --gold:#7a5d20; --gold-soft:#c9a94e; --virgin:#c40808; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#16261a; --paper:#1e3120; --ink:#f5f0e1; --ink2:#d9d2bf; --mute:#a9a795; --line:#2f4632; --green:#7fb46e; --gold:#c9a94e; --gold-soft:#e8d48b; --virgin:#ff6b6b; }} }}
:root[data-theme="dark"] {{ --bg:#16261a; --paper:#1e3120; --ink:#f5f0e1; --ink2:#d9d2bf; --mute:#a9a795; --line:#2f4632; --green:#7fb46e; --gold:#c9a94e; --gold-soft:#e8d48b; --virgin:#ff6b6b; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Inter","Helvetica Neue",Arial,sans-serif; font-size:10.4px; line-height:1.38; padding-inline:16px; padding-block:24px; }}
.page {{ max-width: 210mm; margin: 0 auto; background: var(--paper); padding: 11mm 12mm 10mm; box-shadow: 0 2px 20px rgba(0,0,0,.08); }}
.eyebrow {{ font-size:8px; letter-spacing:.2em; text-transform:uppercase; color:var(--gold); font-weight:700; }}
h1 {{ font-family:"PosterGothic",Impact,"Arial Narrow",sans-serif; font-weight:800; text-transform:uppercase; font-size:26px; line-height:.95; margin:4px 0 6px; letter-spacing:.01em; }}
h2 {{ font-family:"PosterGothic",Impact,"Arial Narrow",sans-serif; text-transform:uppercase; font-size:12.5px; letter-spacing:.03em; margin:11px 0 3px; color:var(--green); }}
h2:first-child {{ margin-top:0; }}
p {{ margin:0 0 5px; }}
.verdict {{ font-size:11.6px; line-height:1.4; color:var(--ink); border-left:3px solid var(--gold-soft); padding-left:10px; margin:6px 0 9px; }}
.stats {{ display:grid; grid-template-columns:repeat(6,1fr); gap:8px; margin:8px 0 10px; }}
.stat b {{ display:block; font-family:"PosterGothic",Impact,sans-serif; font-size:19px; line-height:1; color:var(--ink); font-variant-numeric:tabular-nums; }}
.stat span {{ display:block; font-size:7.6px; color:var(--mute); margin-top:3px; line-height:1.25; }}
.stat {{ border-top:2px solid var(--gold-soft); padding-top:5px; }}
.cols {{ display:grid; grid-template-columns: 1fr 1.08fr; gap: 16px; }}
table {{ border-collapse:collapse; width:100%; font-variant-numeric:tabular-nums; margin:3px 0 8px; font-size:9.3px; }}
th, td {{ padding:2.6px 5px; border-bottom:1px solid var(--line); text-align:right; white-space:nowrap; }}
th {{ font-size:7.6px; letter-spacing:.08em; text-transform:uppercase; color:var(--mute); font-weight:600; }}
th:first-child, td:first-child {{ text-align:left; white-space:normal; }}
ul {{ margin:0; padding-left:13px; }} li {{ margin:0 0 3px; }} li b {{ font-weight:600; }}
.foot {{ font-size:7.6px; color:var(--mute); margin-top:8px; border-top:1px solid var(--line); padding-top:5px; }}
@media (max-width:640px) {{ .cols {{ grid-template-columns:1fr; }} .stats {{ grid-template-columns:repeat(3,1fr); }} .page {{ padding:8mm 6mm; }} }}
@page {{ size: A4; margin: 0; }}
@media print {{ body {{ background:#fff; padding:0; font-size:10.2px; }} .page {{ box-shadow:none; max-width:none; padding:10mm 11mm 8mm; }} }}
</style>
<div class="page">
<div class="eyebrow">One-page financial analysis · Get Lucky Golf × Virgin Active · September 2026 · ZAR ex VAT</div>
<h1>200 Golfzon bays in Virgin Active clubs: is the capital worth it?</h1>
<p class="verdict">Yes, on the base case and on the low case. {m(B['total_capex'])} of bays financed 90% by RMB pays for itself from bay EBITDA in {payback} and covers its own debt {R(B,2031)['dscr']:.1f} times over at maturity. Get Lucky Golf's equity exposure is {m(eq(B))} in the base case and {m(eq(Lc))} in the low case, against cash after debt of {m(cum_cash(B))} by 2032. Virgin Active earns {m(R(B,2031)['va_share'])} a year for no capital. The whole case rests on one number: booked hours a bay a day.</p>
<div class="stats">
  <div class="stat"><b>{m(B['total_capex'])}</b><span>Capex, 200 bays in 130 clubs, 2027–29</span></div>
  <div class="stat"><b>{m(B['debt_total'])}</b><span>RMB facility, prime + 1.5%, 12 months interest-only then 60 amortising</span></div>
  <div class="stat"><b>{m(eq(B))}</b><span>Equity needed, base case (low {m(eq(Lc))})</span></div>
  <div class="stat"><b>{m(R(B,2031)['ebitda'])}</b><span>EBITDA 2031 at {pct(R(B,2031)['ebitda']/R(B,2031)['revenue'])} margin on {m(R(B,2031)['revenue'])} revenue</span></div>
  <div class="stat"><b>{R(B,2031)['dscr']:.1f}×</b><span>Debt cover 2031, base (low {R(Lc,2031)['dscr']:.1f}×)</span></div>
  <div class="stat"><b>{pct(proj_irr)}</b><span>Unlevered project IRR, six years, no terminal value</span></div>
</div>
<div class="cols">
<div>
<h2>The opportunity</h2>
<p>A ten-year exclusive concession to put two Golfzon bays in 70 Virgin Active clubs and one in 60 smaller clubs, booked like padel at R360 to R520 an hour, with a R299 a month golf add-on on the member bill. Get Lucky Golf owns and runs the bays. RMB finances the equipment against the bays and the concession. Virgin Active provides the room and 623,000 members and takes 20% of bay revenue. Virgin Golf is the concept name; the Virgin marks stay Virgin's.</p>
<h2>Why the capital is worth it</h2>
<ul>
<li><b>A bay repays itself in under two years.</b> A metro Play bay costs {k(U['Play']['capex'])} landed and earns {k(U['Play']['ebitda'])} of EBITDA at five booked hours a day, {k(U['Play']['cash_after_debt'])} after RMB. Golfzon's own venue guidance is ten hours a day at $50; the base case is half the hours at a third of the rate.</li>
<li><b>The chain earns {m(cum_ebitda)} of EBITDA in six years</b> on {m(B['total_capex'])} of capex, and pays RMB {m(cum_ds)} of interest and capital out of that. Unlevered project IRR is {pct(proj_irr)} with no terminal value; 2032 EBITDA of {m(R(B,2032)['ebitda'])} is what a buyer would price.</li>
<li><b>Gearing does the work.</b> Because bay cash flow services 90% debt from year two, Get Lucky Golf's equity is {m(eq(B))}, the phase-one deposit and the first half-year. Later deposits come out of bay cash. Cash after debt and deposits reaches {m(cum_cash(B))} by 2032.</li>
<li><b>Virgin Active's side is clean.</b> {m(cum_va)} over six years, {m(R(B,2031)['va_share'])} a year at maturity, for space inside refurbishments it has budgeted, with no capital, debt or operating cost. That is what makes the concession grantable.</li>
</ul>
<h2>Where it breaks</h2>
<p>Debt cover falls to 1.0× at {be10[0]:.1f} booked hours a bay a day ({m(be10[1])} revenue) and to a bank's usual 1.3× floor at {be13[0]:.1f} hours. The low case at 3.5 hours still covers {R(Lc,2031)['dscr']:.1f}× but needs {m(eq(Lc))} of equity to get through 2028, when phases one and two are ramping and 140 bays are being serviced on part-year revenue. That ramp gap, not maturity, is the financing risk.</p>
<h2>Risks that matter</h2>
<ul>
<li><b>Use.</b> Every other line is small. Padel at R400 an hour and the Point's existing simulator are the evidence; the reference zone in Johannesburg in 2027 is the proof, before phase two is drawn.</li>
<li><b>The two posts.</b> Giving Virgin Active 25% costs about R9m a year of EBITDA at maturity; building the shell ourselves adds R30m of capex and R6m of equity. Every combination still services RMB except 25% and we build, at 1.3× on the low case.</li>
<li><b>Platform.</b> Virgin Active's two existing bays are TrackMan. Standardising the chain on Golfzon is the pitch; Golfzon pricing is indicative until the October quote.</li>
<li><b>Brand.</b> The Virgin name is theirs to grant. The economics do not depend on it; the door does.</li>
<li><b>Equity source.</b> {m(eq(B))} to {m(eq(Lc))}: the Get Lucky round, a co-investor, Golfzon supplier credit or a naming partner paid up front. RMB will ask first.</li>
</ul>
</div>
<div>
{unit_tbl()}
{chain_tbl()}
{cases_tbl()}
{mix_tbl()}
</div>
</div>
<div class="foot">Sources and status: Virgin Active published figures to March 2026; Golfzon published commercial ranges and room specifications; Virgin Active padel and South African simulator venue rates, September 2026; SA prime 10.5%. Utilisation, yields, add-on take-up, cost lines and RMB terms are Get Lucky Golf working assumptions, each an input in the model workbook. Forecasts, not a guarantee. Not yet an agreement with Virgin Active, Virgin Group, Golfzon or RMB.</div>
</div>
"""
open("onepager.html", "w").write(page); print("wrote onepager.html", len(page) // 1024, "KB")
