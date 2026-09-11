"""Render the model review page from model.json. Run after model.py."""
import json, base64, html
d = json.load(open("model.json"))
B = d["cases"]["base"]; L = d["cases"]["low"]; H = d["cases"]["high"]
U = d["unit"]; UL = d["unit_low"]
font = base64.b64encode(open("../golfzon/fonts/PosterGothicRoundATF-Heavy.woff2", "rb").read()).decode()

def m(x, dp=1): return ("−" if x < 0 else "") + f"R{abs(x)/1e6:.{dp}f}m"
def k(x): return f"R{x/1e3:,.0f}k"
def r(x): return f"R{x:,.0f}"
def pct(x): return f"{x*100:.0f}%"
def row(y, C): return C["rows"][str(y)]
mature = row(2031, B); lo31 = row(2031, L); hi31 = row(2031, H)
trough = lambda C: min(C["rows"][str(y)]["cum_cash"] for y in C["years"])
clubs = sum(p["clubs"] for p in d["phases"]); bays = sum(sum(p["units"].values()) for p in d["phases"])
addon_members = clubs * d["members_per_club"] * d["addon_adoption"]
hours31 = mature["hours"]

def unit_table():
    types = ["Signature", "Play", "Practice"]
    lines = [
        ("Hardware, Golfzon list", lambda u: f"${u['hw_usd']:,}"),
        ("Landed and installed, per bay", lambda u: k(u["capex"])),
        ("Booked hours a day", lambda u: f"{u['hours']/360:.1f}"),
        ("Blended yield per booked hour", lambda u: r(u["yld"])),
        ("Bay hire", lambda u: k(u["bay_hire"])),
        ("Golf membership add-on, allocated", lambda u: k(u["membership"])),
        ("Leagues, events, corporate", lambda u: k(u["leagues"])),
        ("Get Lucky insured shot, net of premium", lambda u: k(u["challenge"])),
        ("Naming partner", lambda u: k(u["sponsorship"])),
        ("<b>Revenue</b>", lambda u: f"<b>{k(u['revenue'])}</b>"),
        ("Virgin Active concession, 20%", lambda u: f"<span class='va'>({k(u['va_share'])})</span>"),
        ("Golfzon service and software", lambda u: f"({k(u['costs']['golfzon'])})"),
        ("Consumables, card fees, marketing, insurance", lambda u: f"({k(u['costs']['consumables']+u['costs']['card']+u['costs']['marketing']+u['costs']['asset_ins'])})"),
        ("People and central, allocated", lambda u: f"({k(u['costs']['people_central'])})"),
        ("<b>EBITDA</b>", lambda u: f"<b>{k(u['ebitda'])}</b> <span class='mute'>{pct(u['margin'])}</span>"),
        ("RMB instalments, full year", lambda u: f"({k(u['debt_service'])})"),
        ("<b>Cash after debt</b>", lambda u: f"<b>{k(u['cash_after_debt'])}</b>"),
        ("Payback on capex, from EBITDA", lambda u: f"{u['payback_years']:.1f} years"),
    ]
    h = "<table><thead><tr><th>Per bay, mature year, base case</th>" + "".join(f"<th>{t}<small>{U[t]['label']}</small></th>" for t in types) + "</tr></thead><tbody>"
    for label, f in lines:
        h += f"<tr><td>{label}</td>" + "".join(f"<td class='n'>{f(U[t])}</td>" for t in types) + "</tr>"
    return h + "</tbody></table>"

def chain_table(C, title):
    ys = C["years"]
    cols = [
        ("Bays live", lambda x: f"{x['bays']}"),
        ("Booked hours a bay a day", lambda x: f"{x['hours']/x['bays']/360:.1f}"),
        ("Revenue", lambda x: m(x["revenue"])),
        ("Virgin Active share", lambda x: f"<span class='va'>{m(x['va_share'])}</span>"),
        ("EBITDA", lambda x: m(x["ebitda"])),
        ("Margin", lambda x: pct(x["ebitda"]/x["revenue"])),
        ("RMB interest and capital", lambda x: m(x["debt_service"])),
        ("Debt cover", lambda x: f"{x['dscr']:.2f}×"),
        ("Cash after debt", lambda x: m(x["cash_after_debt"])),
        ("Equity in", lambda x: m(x["equity_in"]) if x["equity_in"] else "–"),
        ("Cumulative cash", lambda x: m(x["cum_cash"])),
    ]
    h = f"<table><thead><tr><th>{title}</th>" + "".join(f"<th>{y}</th>" for y in ys) + "</tr></thead><tbody>"
    for label, f in cols:
        h += f"<tr><td>{label}</td>" + "".join(f"<td class='n'>{f(row(y, C))}</td>" for y in ys) + "</tr>"
    return h + "</tbody></table>"

cases_tbl = "<table><thead><tr><th>2031, the first full year at 200 bays</th><th>Low<small>70% of base use</small></th><th>Base</th><th>High<small>125% of base use</small></th></tr></thead><tbody>"
for label, f in [
    ("Booked hours a bay a day", lambda x: f"{x['hours']/200/360:.1f}"),
    ("Revenue", lambda x: m(x["revenue"])),
    ("Virgin Active share", lambda x: f"<span class='va'>{m(x['va_share'])}</span>"),
    ("EBITDA", lambda x: m(x["ebitda"])),
    ("Debt cover", lambda x: f"{x['dscr']:.2f}×"),
    ("Cash after debt", lambda x: m(x["cash_after_debt"])),
]:
    cases_tbl += f"<tr><td>{label}</td>" + "".join(f"<td class='n'>{f(row(2031, C))}</td>" for C in (L, B, H)) + "</tr>"
cases_tbl += f"<tr><td>Lowest point of cumulative cash</td>" + "".join(f"<td class='n'>{m(trough(C))}</td>" for C in (L, B, H)) + "</tr>"
cases_tbl += "<tr><td>Equity needed, deposits and ramp together</td>" + "".join(f"<td class='n'><b>{m(-trough(C))}</b></td>" for C in (L, B, H)) + "</tr>"
cases_tbl += "</tbody></table>"

order_tbl = "<table><thead><tr><th>Phase</th><th>When</th><th>Bays</th><th>Clubs</th><th>Capex</th><th>RMB, 90%</th><th>Equity, 10%</th></tr></thead><tbody>"
for p, c in zip(d["phases"], B["capex_by_phase"]):
    units = ", ".join(f"{n} {t}" for t, n in p["units"].items())
    order_tbl += f"<tr><td>{p['name']}</td><td>{p['year']}</td><td>{units}</td><td class='n'>{p['clubs']}</td><td class='n'>{m(c)}</td><td class='n'>{m(c*0.9)}</td><td class='n'>{m(c*0.1)}</td></tr>"
order_tbl += f"<tr class='total'><td>Total</td><td>2027–29</td><td>{bays} bays</td><td class='n'>{clubs}</td><td class='n'>{m(B['total_capex'])}</td><td class='n'>{m(B['debt_total'])}</td><td class='n'>{m(B['equity_total'])}</td></tr></tbody></table>"

grid = d["negotiation"]
grid_tbl = "<table><thead><tr><th>2031, base case</th><th>Shell built by</th><th>Virgin Active share</th><th>Capex</th><th>To Virgin Active</th><th>Get Lucky Golf EBITDA</th><th>Debt cover<small>base · low case</small></th><th>Equity needed</th></tr></thead><tbody>"
for g in grid:
    opening = g["shell_by"] == "Virgin Active" and abs(g["share"] - 0.20) < 1e-9
    cls = " class='total'" if opening else ""
    label = "Opening position" if opening else ""
    grid_tbl += f"<tr{cls}><td>{label}</td><td>{g['shell_by']}</td><td class='n'>{pct(g['share'])}</td><td class='n'>{m(g['capex'],0)}</td><td class='n'><span class='va'>{m(g['va_income'],0)}</span></td><td class='n'>{m(g['ebitda'],0)}</td><td class='n'>{g['dscr']:.2f}× · {g['dscr_low']:.2f}×</td><td class='n'>{m(g['equity_need'],0)}</td></tr>"
grid_tbl += "</tbody></table>"

two_bay = U["Play"]["va_share"] * 2; sig_zone = U["Signature"]["va_share"] * 2; one_bay = U["Play"]["va_share"]

page = f"""<title>Virgin Golf Bay Model</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>
@font-face {{ font-family: "PosterGothic"; src: url(data:font/woff2;base64,{font}) format("woff2"); font-weight: 800; font-display: swap; }}
:root {{
  --bg: #f5f0e1; --bg2: #ede6d2; --ink: #16261a; --ink2: #3d4a3f; --mute: #6b746c; --line: #d6ccb2;
  --green: #335231; --green-light: #4a7a3d; --gold: #7a5d20; --gold-soft: #c9a94e; --virgin: #c40808; --virgin-soft: rgba(196,8,8,.08);
  --display: "PosterGothic", Impact, "Arial Narrow", sans-serif; --sans: "Inter", "Helvetica Neue", Arial, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #16261a; --bg2: #1e3120; --ink: #f5f0e1; --ink2: #d9d2bf; --mute: #a9a795; --line: #2f4632;
  --green: #4a7a3d; --green-light: #7fb46e; --gold: #c9a94e; --gold-soft: #e8d48b; --virgin: #ff4d4d; --virgin-soft: rgba(255,77,77,.12);
}} }}
:root[data-theme="dark"] {{
  --bg: #16261a; --bg2: #1e3120; --ink: #f5f0e1; --ink2: #d9d2bf; --mute: #a9a795; --line: #2f4632;
  --green: #4a7a3d; --green-light: #7fb46e; --gold: #c9a94e; --gold-soft: #e8d48b; --virgin: #ff4d4d; --virgin-soft: rgba(255,77,77,.12);
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 16px; line-height: 1.55; padding-inline: 20px; padding-block: 40px 80px; }}
.wrap {{ max-width: 62rem; margin: 0 auto; }}
h1, h2 {{ font-family: var(--display); font-weight: 800; text-transform: uppercase; line-height: .95; letter-spacing: .01em; margin: 0; text-wrap: balance; color: var(--ink); }}
h1 {{ font-size: clamp(2.4rem, 7vw, 4.4rem); }}
h2 {{ font-size: clamp(1.5rem, 3.4vw, 2.2rem); margin-top: 3.2rem; }}
h3 {{ font-size: 1rem; margin: 0 0 .4rem; }}
p {{ margin: .6rem 0 0; max-width: 40rem; }}
.eyebrow {{ font-size: .72rem; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: .9rem; }}
.lede {{ font-size: 1.15rem; color: var(--ink2); max-width: 44rem; margin-top: 1.2rem; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; margin-top: 2rem; }}
.stat {{ border-top: 3px solid var(--gold-soft); padding-top: .6rem; }}
.stat b {{ display: block; font-family: var(--display); font-size: 2.1rem; line-height: 1; color: var(--ink); font-variant-numeric: tabular-nums; }}
.stat span {{ display: block; font-size: .8rem; color: var(--mute); margin-top: .35rem; }}
.stat.va {{ border-color: var(--virgin); }}
.parties {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 1.4rem; }}
.party {{ background: var(--bg2); padding: 18px 20px 20px; border-top: 3px solid var(--green); }}
.party.p-va {{ border-top-color: var(--virgin); }}
.party.rmb {{ border-top-color: var(--gold-soft); }}
.party h3 {{ font-family: var(--display); text-transform: uppercase; font-size: 1.3rem; letter-spacing: .02em; }}
.party dl {{ margin: .8rem 0 0; }}
.party dt {{ font-size: .7rem; letter-spacing: .16em; text-transform: uppercase; color: var(--mute); margin-top: .8rem; }}
.party dd {{ margin: .2rem 0 0; font-size: .93rem; }}
.tbl {{ overflow-x: auto; margin-top: 1.2rem; }}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; font-variant-numeric: tabular-nums; }}
th, td {{ text-align: left; padding: .5rem .7rem; border-bottom: 1px solid var(--line); vertical-align: top; white-space: nowrap; }}
th {{ font-size: .74rem; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); font-weight: 600; }}
th small {{ display: block; text-transform: none; letter-spacing: 0; font-weight: 400; margin-top: .15rem; white-space: normal; max-width: 12rem; }}
td.n, th:not(:first-child) {{ text-align: right; }}
td:first-child {{ white-space: normal; min-width: 14rem; }}
tr.total td {{ font-weight: 700; border-top: 2px solid var(--ink); }}
.va {{ color: var(--gold); font-weight: 600; }} .mute {{ color: var(--mute); }}
ul {{ padding-left: 1.2rem; margin: .8rem 0 0; max-width: 44rem; }} li {{ margin-top: .45rem; }}
li b {{ font-weight: 600; }}
.note {{ font-size: .86rem; color: var(--mute); margin-top: .8rem; max-width: 44rem; }}
.decide {{ counter-reset: q; list-style: none; padding: 0; }}
.decide li {{ counter-increment: q; padding: .8rem 0; border-top: 1px solid var(--line); display: grid; grid-template-columns: 2.2rem 1fr; gap: .6rem; }}
.decide li::before {{ content: counter(q); font-family: var(--display); font-size: 1.5rem; color: var(--gold); line-height: 1; }}
.decide li:last-child {{ border-bottom: 1px solid var(--line); }}
@media (max-width: 480px) {{ body {{ padding-block: 28px 60px; }} }}
</style>
<div class="wrap">
<p class="eyebrow">Working draft for Johannes · September 2026 · not yet for Virgin Active or RMB</p>
<h1>The Virgin Golf bay model</h1>
<p class="lede">One model, two readers. Virgin Active reads it to see what 200 bays earn a chain that puts up no capital. RMB reads it to see the same cash servicing a {m(B['debt_total'],0)} asset-finance facility. Every number below comes out of <code>virginactive/model.py</code>, so a changed assumption changes the whole page.</p>
<div class="stats">
  <div class="stat"><b>{m(B['total_capex'],0)}</b><span>200 bays landed and installed, 2027–29</span></div>
  <div class="stat"><b>{m(B['debt_total'],0)}</b><span>RMB facility at prime + 1.5%, 90% of capex</span></div>
  <div class="stat"><b>{m(mature['revenue'],0)}</b><span>Revenue in 2031, first full year at 200 bays</span></div>
  <div class="stat"><b>{mature['dscr']:.1f}×</b><span>Debt cover in 2031, base case</span></div>
  <div class="stat va"><b>{m(mature['va_share'],0)}</b><span>To Virgin Active in 2031, for no capital</span></div>
</div>

<h2>The structure</h2>
<p>Get Lucky Golf, with Ernie Els as founding partner, buys, installs and operates 200 Golfzon bays inside Virgin Active clubs under a ten-year exclusive concession. Virgin Golf is the concept name proposed for the zones; the Virgin marks are Virgin Group's, so the name is theirs to grant and Get Lucky Golf never owns it. RMB finances the equipment against the concession agreement and the bays themselves. Virgin Active provides the room, the power and its members, bills the golf membership add-on on the member's account, and takes a fifth of every rand the bays earn.</p>
<div class="parties">
  <div class="party p-va"><h3>Virgin Active</h3><dl>
    <dt>Puts in</dt><dd>A two-bay zone of about 60 m² in 70 clubs and a single bay of about 30 m² in 60 smaller clubs, built into planned refurbishments. Power, cleaning, access control. Bay booking in the Virgin Active app. Marketing to 623,000 members. A ten-year exclusive.</dd>
    <dt>Gets out</dt><dd>20% of bay revenue: <b class="va">{m(mature['va_share'],0)} a year</b> at maturity, about {k(two_bay)} a year for a two-bay zone, {k(sig_zone)} for a two-bay Collection zone and {k(one_bay)} for a single bay, with no capital and no operating risk. A member retention product. Ernie Els on the door. First call on Get Lucky Golf for the UK, Italy, Australia and Asia.</dd>
  </dl></div>
  <div class="party"><h3>Get Lucky Golf</h3><dl>
    <dt>Puts in</dt><dd>Equity of about <b>{m(-trough(B),0)} in the base case</b>, {m(-trough(L),0)} in the low case: the phase-one deposit and the 2027 ramp. The phase-two and phase-three deposits are paid out of bay cash flow. The Golfzon relationship, the Ernie Els brand, coaching content, leagues, the insured-shot product, operations and a golf host in every Collection club.</dd>
    <dt>Gets out</dt><dd>EBITDA of {m(mature['ebitda'],0)} a year at maturity, {m(mature['cash_after_debt'],0)} after RMB. Payback on a bay from its own EBITDA in under two years. A 200-bay reference customer to take to Golfzon and to the rest of the Virgin Active group.</dd>
  </dl></div>
  <div class="party rmb"><h3>RMB</h3><dl>
    <dt>Puts in</dt><dd>{m(B['debt_total'],0)} in three phased drawdowns, each 12 months interest-only while the phase commissions and ramps, then 60 months amortising at prime + 1.5% (12.0% today). Security over the bays and a cession of the concession agreement and the naming sponsorship.</dd>
    <dt>Gets out</dt><dd>Debt cover of {row(2029,B)['dscr']:.1f}× in 2029 rising to {mature['dscr']:.1f}× at maturity in the base case, {lo31['dscr']:.1f}× at maturity in the low case. A national fitness chain as the venue, Santam behind the prize product, and equipment that Golfzon services under contract.</dd>
  </dl></div>
</div>

<h2>The order and what it costs</h2>
<p>Golfzon list prices with a 30% landed factor for freight, duties, the enclosure, screen, seating and installation. Virgin Active supplies the room shell and power as part of club refurbishments; if it will not, add roughly R150k a bay.</p>
<div class="tbl">{order_tbl}</div>

<h2>A bay at maturity</h2>
<p>Bay hire is the engine. A bay is bookable 15 hours a day, 360 days a year. The base case has a metro Play bay booked five hours a day at a blended R360 an hour across peak, off-peak, member and non-member rates. Virgin Active padel is R400 an hour today; Johannesburg and Cape Town simulator venues charge R200 to R400 a bay. Golfzon's own venue guidance is ten hours a day at $50; the base case is half the hours at a third of the rate.</p>
<div class="tbl">{unit_table()}</div>
<p class="note">Membership add-on: R299 a month ex VAT on the Virgin Active bill, one included off-peak hour and 20% off bookings, taken up by 1.5% of members at clubs with bays ({addon_members:,.0f} members, R{addon_members*299*12/1e6:.0f}m a year), allocated evenly across the 200 bays. Included hours sit inside the utilisation figure, not on top of it. Coaching runs inside bay hire: the pro books the bay and keeps the lesson fee.</p>

<h2>The chain, 2027 to 2032</h2>
<p>Phase one lands mid-2027, so 2027 is half a year of 40 bays at 55% of mature use. A bay reaches 80% of mature use in its second year and 100% in its third. The chain is complete in 2029 and fully ramped in 2031.</p>
<div class="tbl">{chain_table(B, "Base case")}</div>
<p class="note">Cumulative cash is after the 10% deposits and RMB instalments, before tax. The low point is the equity the project needs. The base case is cash positive from 2028 and has repaid its own equity by 2029.</p>

<h2>Three cases</h2>
<p>Use is the only assumption that matters. The low case cuts booked hours and add-on take-up to 70% of base, which is 3.5 hours a bay a day. It still covers RMB 1.6 times at maturity; it just needs more equity to get through 2028.</p>
<div class="tbl">{cases_tbl}</div>

<h2>The two movable posts</h2>
<p>Two terms are Virgin Active's to negotiate and ours to move: its share of bay revenue, and who builds the room shell. The opening position is 20% and Virgin Active builds, inside refurbishments it has already budgeted. Every combination below still covers RMB, so both posts can move to make the deal work. Giving Virgin Active 25% costs Get Lucky Golf about R9m a year of EBITDA at maturity; building the shell ourselves adds R{d['shell_per_bay']/1e3:.0f}k a bay, R30m to the facility and R6m to the equity.</p>
<div class="tbl">{grid_tbl}</div>
<p class="note">Debt cover is the 2031 figure. Equity needed is the low point of cumulative cash, base case. The bank's floor is usually 1.3× on the low case; every cell clears it except 25% with Get Lucky Golf building, which sits at 1.26×.</p>

<h2>What Virgin Active sees</h2>
<ul>
  <li><b>{m(mature['va_share'],0)} a year</b> of concession income across {clubs} clubs at maturity, for space it is refurbishing anyway. That is about {k(two_bay)} a year from a two-bay zone, {k(sig_zone)} from a two-bay Collection zone and {k(one_bay)} from a single bay.</li>
  <li><b>{hours31/1e3:,.0f}k booked bay-hours a year</b>, roughly {hours31*2.5/1e6:.1f} million player visits. Every one is a member reason to come to the club on a winter weeknight.</li>
  <li><b>{addon_members:,.0f} members on a golf add-on</b> at R299 a month, billed by Virgin Active, with a share to Virgin Active and a reason not to cancel.</li>
  <li><b>Zero capital, zero operating risk.</b> RMB carries the equipment, Golfzon services it, Get Lucky Golf runs it. Virgin Active can take a buy-out option on the bays at the end of the concession if it wants them.</li>
</ul>

<h2>Assumptions and where they come from</h2>
<ul>
  <li><b>Golfzon hardware</b>: TwoVision NX $60,000, Vision Standard $35,000, GDR Plus $22,000, from Golfzon's published commercial ranges ($25k to $90k a bay). To be replaced by the Golfzon quote in October.</li>
  <li><b>Rates</b>: Virgin Active padel R400 an hour; South African simulator venues R200 to R400 a bay an hour (Par 72, Golf Bar, Golf Sim Centre). Blended yields: Signature R520, Play R360, Practice R240.</li>
  <li><b>Use</b>: 6.0, 5.0 and 4.5 booked hours a day by bay type at maturity. Golfzon's venue guidance is 10 hours a day.</li>
  <li><b>Virgin Active</b>: 136 Southern African clubs, 623,000 members (published, March 2026), so 4,580 members a club. {clubs} clubs take bays: two in 70, one in 60. Golfzon's TwoVision NX bay is about 5.6 m by 5.5 m with a 3.1 m ceiling, so a two-bay zone is about 60 m² and a single bay about 30 m².</li>
  <li><b>RMB</b>: prime 10.5% (August 2026) plus 1.5%; 12 months interest-only then 60 amortising, per phase; 90% of landed cost financed.</li>
  <li><b>Costs</b>: Golfzon software, courses and service at 4% of hardware a year; consumables R24k a bay; card fees 2.5%; marketing 5% of revenue; asset insurance 1% of capex; people R12m a year at maturity (a golf host in each Collection and flagship club, four regional technicians, a small central team) and R4m central overhead.</li>
  <li><b>Insured shot</b>: R50 for R25,000, one in four players in a bay-hour takes one, 24% ceded to Santam, per the Get Lucky model. Small in rand terms, the whole story in brand terms.</li>
  <li><b>FX</b> 18.5, as in the investor model. All figures ex VAT. Depreciation over seven years and tax at 27% are not shown; EBITDA and debt service are what the two readers look at first.</li>
</ul>

<h2>Decisions</h2>
<ol class="decide">
  <li><span><b>Settled: the share and the shell are the negotiation.</b> Open at 20% of bay revenue with Virgin Active building the shell and power inside its refurbishments. Both posts move as needed; the grid above shows what each move costs and that every combination still services RMB.</span></li>
  <li><span><b>Equity.</b> {m(-trough(B),0)} base, {m(-trough(L),0)} low, most of it in 2027 for the phase-one deposit of {m(B['capex_by_phase'][0]*0.1,1)} and the first half-year. Sources: the Get Lucky round, a Get Lucky Golf co-investor, Golfzon supplier credit on phase one, or a naming partner paying up front. This is the question RMB will ask first.</span></li>
  <li><span><b>The membership add-on.</b> R299 a month with one included hour. Virgin Active may want it inside its Collection tier instead. Either way it is billed by Virgin Active.</span></li>
  <li><span><b>Naming partner.</b> R25k a bay a year is deliberately modest. Santam, RMB itself, or a beverage brand could take the chain naming at a multiple of that.</span></li>
  <li><span><b>Term and exit.</b> Ten-year exclusive with a Virgin Active buy-out option at year five or ten. RMB's facility runs six years per phase, so the concession must outlast it.</span></li>
  <li><span><b>Group rights.</b> First refusal on the UK, Italy, Australia and Asia for Get Lucky Golf, with each territory financed on its own numbers.</span></li>
</ol>
<p class="note">Virgin Golf by Ernie Els is a concept proposed by Get Lucky Golf Club (Pty) Ltd with Ernie Els; the Virgin marks belong to Virgin Group and the name is theirs to grant. Not yet an agreement with Virgin Active, Virgin Group, Golfzon or RMB. Every forward figure is a forecast built on the stated assumptions.</p>
</div>
"""
open("review.html", "w").write(page)
print("wrote review.html", len(page))
