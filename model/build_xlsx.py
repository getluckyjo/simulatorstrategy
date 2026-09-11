"""Build the Virgin Golf bay model as an Excel workbook with live formulas, mirroring model.py."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

d = json.load(open("model.json"))
FONT = "Arial"
BLUE = Font(name=FONT, color="0000FF"); BLACK = Font(name=FONT); GREEN = Font(name=FONT, color="008000")
BOLD = Font(name=FONT, bold=True); H1 = Font(name=FONT, bold=True, size=14); H2 = Font(name=FONT, bold=True, size=11, color="335231")
YELLOW = PatternFill("solid", fgColor="FFFF00"); GREY = PatternFill("solid", fgColor="F2F2F2"); GREENFILL = PatternFill("solid", fgColor="E2EFDA")
ZAR = '"R"#,##0;("R"#,##0);-'; ZARM = '"R"#,##0.0,,"m";("R"#,##0.0,,"m");-'; PCT = '0.0%;(0.0%);-'; NUM = '#,##0;(#,##0);-'; DEC = '0.00;(0.00);-'; X = '0.00"×"'
thin = Side(style="thin", color="BFBFBF"); TOP = Border(top=Side(style="thin", color="000000"))

wb = Workbook()

# ---------------- Assumptions ----------------
A = wb.active; A.title = "Assumptions"
A.column_dimensions["A"].width = 46; A.column_dimensions["B"].width = 16; A.column_dimensions["C"].width = 90
for col in "DEFGH": A.column_dimensions[col].width = 14
A["A1"] = "Virgin Golf bay model — Get Lucky Golf × Virgin Active"; A["A1"].font = H1
A["A2"] = "Blue cells are inputs. Black cells are formulas. Green cells link to another sheet. Yellow is the case selector. All money in ZAR ex VAT."; A["A2"].font = Font(name=FONT, italic=True)
names = {}
row = [4]
def sec(title):
    row[0] += 1; A.cell(row[0], 1, title).font = H2; row[0] += 1
def inp(key, label, value, fmt, note="", formula=False, fill=None):
    r = row[0]; A.cell(r, 1, label).font = BLACK
    c = A.cell(r, 2, value); c.font = BLACK if formula else BLUE; c.number_format = fmt
    if fill: c.fill = fill
    if note: A.cell(r, 3, note).font = Font(name=FONT, size=9, color="595959")
    names[key] = f"Assumptions!$B${r}"; row[0] += 1; return r

sec("Case selector")
inp("mult", "Utilisation multiplier in use (1.00 base, 0.70 low, 1.25 high)", 1.0, DEC, "Change this one cell to run the whole model at a different level of use. Booked hours and add-on take-up both scale with it.", fill=YELLOW)
inp("mult_low", "Low case multiplier", 0.70, DEC, "70% of base use: 3.5 booked hours a bay a day at maturity.")
inp("mult_base", "Base case multiplier", 1.00, DEC)
inp("mult_high", "High case multiplier", 1.25, DEC, "125% of base use: 6.3 booked hours a bay a day.")
dv = DataValidation(type="list", formula1='"0.7,1,1.25"', allow_blank=False); A.add_data_validation(dv); dv.add(A["B6"])

sec("Money and financing")
inp("fx", "ZAR per USD", d["fx"], DEC, "Same rate as the Get Lucky investor model.")
inp("prime", "SA prime lending rate", d["prime"], PCT, "10.5% from 28 May 2026, unchanged at the 23 July 2026 MPC. Source: SARB / debtsolutions4u.co.za prime rate tracker, August 2026.")
inp("margin", "RMB margin over prime", 0.015, PCT, "Assumed asset-finance margin. To be replaced by the RMB term sheet.")
inp("rate", "Facility rate", f"={names['prime']}+{names['margin']}", PCT, formula=True)
inp("io", "Interest-only months per phase", d["io_months"], NUM, "Capital holiday while a phase is commissioned and ramps.")
inp("term", "Amortising months per phase, after interest-only", d["term_months"], NUM)
inp("debt_pct", "RMB share of landed capex", d["debt_pct"], PCT, "Get Lucky Golf funds the balance as an equity deposit.")
inp("landed", "Landed factor on Golfzon hardware", d["landed"], DEC, "Freight, duties, enclosure, screen, seating, installation, on top of hardware list price. Assumption; replaced by the Golfzon quote.")
inp("shell", "Room shell cost carried by Get Lucky Golf, per bay", 0, ZAR, "Opening position: Virgin Active builds the shell and power inside its refurbishments, so this is 0. If Get Lucky Golf builds, enter about R150,000. Negotiable.")
inp("shell_alt", "Shell cost per bay if Get Lucky Golf builds (for the negotiation grid)", d["shell_per_bay"], ZAR)

sec("The concession")
inp("va_share", "Virgin Active share of bay revenue", d["va_share"], PCT, "Opening position, negotiable. Applies to bay hire, memberships, leagues and the insured shot; not to sponsorship.")
inp("hours_day", "Bookable hours a day", 15, NUM, "Club hours: about 05:00 to 21:00 weekdays, shorter weekends.")
inp("days", "Bookable days a year", 360, NUM)
inp("hours_yr", "Bookable hours a bay a year", f"={names['hours_day']}*{names['days']}", NUM, formula=True)
inp("util_cap", "Maximum utilisation", 0.85, PCT, "Cap so the high case cannot exceed a physically bookable level.")

sec("Members and the add-on")
inp("members", "Virgin Active members, Southern Africa", 623000, NUM, "Virgin Active published figures to March 2026 (IOL Business Report, Nov 2025; Brait results).")
inp("clubs_total", "Virgin Active clubs, Southern Africa", 136, NUM, "Published figure, March 2026.")
inp("members_club", "Members a club", f"={names['members']}/{names['clubs_total']}", NUM, formula=True)
inp("addon", "Golf add-on, R a month ex VAT, on the Virgin Active bill", d["addon_zar_pm"], ZAR, "One included off-peak hour and 20% off bookings. Included hours sit inside the utilisation figure.")
inp("adoption", "Add-on take-up at maturity, share of members at clubs with bays", d["addon_adoption"], PCT, "Assumption. Scales with the utilisation multiplier.")
inp("adopt0", "Add-on take-up ramp, year a club opens", 0.40, PCT, "Share of mature take-up.")
inp("adopt1", "Add-on take-up ramp, second year", 0.75, PCT)

sec("Other revenue per bay")
inp("leagues", "Leagues, events and corporate, a bay a year at maturity", 40000, ZAR, "Assumption.")
inp("sponsor", "Naming partner, a bay a year", 25000, ZAR, "Deliberately modest. Santam, RMB or a beverage brand could take chain naming at a multiple.")
inp("stake", "Get Lucky insured shot: stake", 50, ZAR, "R50 for a swing at R25,000, as on course.")
inp("take", "Insured shots taken per booked bay-hour", 0.625, DEC, "2.5 players in a bay-hour, one in four takes a shot.")
inp("premium", "Premium ceded to Santam, share of stake", 0.24, PCT, "Same 24% as the on-course product in the investor model.")
inp("challenge_hr", "Insured shot revenue per booked hour, net of premium", f"={names['stake']}*{names['take']}*(1-{names['premium']})", DEC, formula=True)

sec("Operating costs")
inp("card", "Card and booking fees, share of shared revenue", 0.025, PCT)
inp("marketing", "Marketing, share of revenue", 0.05, PCT)
inp("asset_ins", "Asset insurance, share of capex a year", 0.01, PCT)
inp("golfzon", "Golfzon software, courses and service, share of hardware a year", 0.04, PCT, "Assumption; replaced by the Golfzon service contract.")
inp("consumables", "Consumables and maintenance, a bay a year", 24000, ZAR, "Balls, mats, tees, screens, projector lamps.")
inp("people_unit", "People and central overhead allocated per bay in the unit view", f"=16000000/200", ZAR, "R12m people plus R4m central at maturity across 200 bays.", formula=True)

sec("Ramp")
inp("ramp0", "Use in the year a bay is commissioned, share of mature", 0.55, PCT)
inp("ramp1", "Use in the second year, share of mature", 0.80, PCT)
inp("depr", "Depreciation, years (memo only)", 7, NUM)
inp("tax", "Company tax (memo only)", 0.27, PCT, "EBITDA and debt service are shown before tax.")

# Bay types table
row[0] += 1; A.cell(row[0], 1, "Bay types").font = H2; row[0] += 1
hdr = ["Bay", "Hardware, USD list", "Mature utilisation", "Blended yield per booked hour, R", "Units in the order", "Where"]
for j, h in enumerate(hdr): c = A.cell(row[0], 1 + j, h); c.font = BOLD; c.fill = GREY
bay_rows = {}
types = ["Signature", "Play", "Practice"]
units_total = {"Signature": 40, "Play": 120, "Practice": 40}
for t in types:
    row[0] += 1; r = row[0]; b = d["bays"][t]
    A.cell(r, 1, t).font = BLACK
    c = A.cell(r, 2, b["hw_usd"]); c.font = BLUE; c.number_format = '"$"#,##0'
    c = A.cell(r, 3, b["util"]); c.font = BLUE; c.number_format = PCT
    c = A.cell(r, 4, b["yld"]); c.font = BLUE; c.number_format = ZAR
    c = A.cell(r, 5, units_total[t]); c.font = BLUE; c.number_format = NUM
    A.cell(r, 6, b["label"]).font = Font(name=FONT, size=9, color="595959")
    bay_rows[t] = r
A.cell(bay_rows["Signature"], 2).comment = Comment("Golfzon commercial ranges published at $25k to $90k a bay (golfzongolf.com, rggolf.com 2026 comparison). TwoVision NX $60k, Vision Standard $35k, GDR Plus $22k are working assumptions until Golfzon quotes.", "Model")
A.cell(bay_rows["Play"], 4).comment = Comment("Virgin Active padel is R400 an hour. Cape Town and Johannesburg simulator venues charge R200 to R400 a bay an hour (Par 72, Golf Bar, Golf Sim Centre). Yields are blended across peak, off-peak, member and non-member rates.", "Model")
A.cell(bay_rows["Signature"], 3).comment = Comment("Golfzon's own venue guidance is 10 booked hours a day. Base case is 6.0 / 5.0 / 4.5 hours by bay type.", "Model")

# Phases table
row[0] += 2; A.cell(row[0], 1, "Phases").font = H2; row[0] += 1
hdr = ["Phase", "Commissioned", "Share of that year live", "Signature units", "Play units", "Practice units", "Clubs"]
for j, h in enumerate(hdr): c = A.cell(row[0], 1 + j, h); c.font = BOLD; c.fill = GREY
phase_rows = []
for p in d["phases"]:
    row[0] += 1; r = row[0]
    A.cell(r, 1, p["name"]).font = BLACK
    c = A.cell(r, 2, p["year"]); c.font = BLUE; c.number_format = "0"
    c = A.cell(r, 3, p["live"]); c.font = BLUE; c.number_format = PCT
    for j, t in enumerate(types):
        c = A.cell(r, 4 + j, p["units"].get(t, 0)); c.font = BLUE; c.number_format = NUM
    c = A.cell(r, 7, p["clubs"]); c.font = BLUE; c.number_format = NUM
    phase_rows.append(r)
A.cell(phase_rows[0], 3).comment = Comment("Phase one lands mid-year, so 50% of 2027 is live. Two bays a club in 70 clubs, one bay in 60 smaller clubs.", "Model")

# People and central by year
row[0] += 2; A.cell(row[0], 1, "Fixed costs by year").font = H2; row[0] += 1
years = list(range(2027, 2033))
A.cell(row[0], 1, "Year").font = BOLD
for j, y in enumerate(years): c = A.cell(row[0], 2 + j, str(y)); c.font = BOLD; c.fill = GREY
yr_hdr_row = row[0]
row[0] += 1; people_row = row[0]; A.cell(row[0], 1, "People: hosts in Collection and flagship clubs, four regional technicians, a small central team").font = BLACK
for j, y in enumerate(years): c = A.cell(row[0], 2 + j, {2027: 4e6, 2028: 8e6, 2029: 11e6}.get(y, 12e6)); c.font = BLUE; c.number_format = ZAR
row[0] += 1; central_row = row[0]; A.cell(row[0], 1, "Central overhead").font = BLACK
for j, y in enumerate(years): c = A.cell(row[0], 2 + j, {2027: 2e6, 2028: 3e6}.get(y, 4e6)); c.font = BLUE; c.number_format = ZAR

def bay(t, col): return f"Assumptions!${L(col)}${bay_rows[t]}"   # 2 hw, 3 util, 4 yield, 5 units
def ph(i, col): return f"Assumptions!${L(col)}${phase_rows[i]}"   # 2 year, 3 live, 4-6 units, 7 clubs

# ---------------- Unit economics ----------------
U = wb.create_sheet("Unit economics")
U.column_dimensions["A"].width = 48
for col in "BCD": U.column_dimensions[col].width = 18
U["A1"] = "A bay at maturity, at the multiplier in use"; U["A1"].font = H1
U["A2"] = "Per bay, per year, ZAR ex VAT. Membership, people and central are allocated evenly across the 200 bays."; U["A2"].font = Font(name=FONT, italic=True)
for j, t in enumerate(types): c = U.cell(4, 2 + j, t); c.font = BOLD; c.fill = GREY
U.cell(4, 1, "").fill = GREY
urow = {}
def uline(key, label, fmts, fmt=ZAR, bold=False, top=False):
    r = len(urow) + 5; urow[key] = r
    c = U.cell(r, 1, label); c.font = BOLD if bold else BLACK
    for j, t in enumerate(types):
        c = U.cell(r, 2 + j, fmts(t, L(2 + j))); c.number_format = fmt; c.font = BOLD if bold else BLACK
        if top: c.border = TOP
    return r
uline("hw", "Hardware, ZAR", lambda t, c: f"={bay(t,2)}*{names['fx']}")
uline("capex", "Landed and installed, plus any shell cost carried", lambda t, c: f"={c}{urow['hw']}*{names['landed']}+{names['shell']}")
uline("util", "Utilisation in use", lambda t, c: f"=MIN({bay(t,3)}*{names['mult']},{names['util_cap']})", PCT)
uline("hours", "Booked hours a year", lambda t, c: f"={names['hours_yr']}*{c}{urow['util']}", NUM)
uline("hpd", "Booked hours a day", lambda t, c: f"={c}{urow['hours']}/{names['days']}", DEC)
uline("yld", "Blended yield per booked hour", lambda t, c: f"={bay(t,4)}")
uline("hire", "Bay hire", lambda t, c: f"={c}{urow['hours']}*{c}{urow['yld']}")
uline("memb", "Golf add-on, allocated per bay", lambda t, c: f"=(Assumptions!$G${phase_rows[0]}+Assumptions!$G${phase_rows[1]}+Assumptions!$G${phase_rows[2]})*{names['members_club']}*{names['adoption']}*{names['mult']}*{names['addon']}*12/SUM(Assumptions!$E${bay_rows['Signature']}:$E${bay_rows['Practice']})")
uline("leagues", "Leagues, events, corporate", lambda t, c: f"={names['leagues']}")
uline("chal", "Get Lucky insured shot, net of premium", lambda t, c: f"={c}{urow['hours']}*{names['challenge_hr']}")
uline("spons", "Naming partner", lambda t, c: f"={names['sponsor']}")
uline("rev", "Revenue", lambda t, c: f"=SUM({c}{urow['hire']}:{c}{urow['spons']})", bold=True, top=True)
uline("va", "Virgin Active concession", lambda t, c: f"=-({c}{urow['rev']}-{c}{urow['spons']})*{names['va_share']}")
uline("card", "Card and booking fees", lambda t, c: f"=-({c}{urow['rev']}-{c}{urow['spons']})*{names['card']}")
uline("mkt", "Marketing", lambda t, c: f"=-{c}{urow['rev']}*{names['marketing']}")
uline("gz", "Golfzon service and software", lambda t, c: f"=-{c}{urow['hw']}*{names['golfzon']}")
uline("cons", "Consumables and maintenance", lambda t, c: f"=-{names['consumables']}")
uline("ins", "Asset insurance", lambda t, c: f"=-{c}{urow['capex']}*{names['asset_ins']}")
uline("people", "People and central, allocated", lambda t, c: f"=-{names['people_unit']}")
uline("ebitda", "EBITDA", lambda t, c: f"=SUM({c}{urow['rev']}:{c}{urow['people']})", bold=True, top=True)
uline("margin", "EBITDA margin", lambda t, c: f"=IF({c}{urow['rev']}=0,0,{c}{urow['ebitda']}/{c}{urow['rev']})", PCT)
uline("debt", "RMB instalments, full amortising year", lambda t, c: f"=-({c}{urow['capex']}*{names['debt_pct']})*({names['rate']}/12)/(1-(1+{names['rate']}/12)^-{names['term']})*12")
uline("cash", "Cash after debt", lambda t, c: f"={c}{urow['ebitda']}+{c}{urow['debt']}", bold=True, top=True)
uline("payback", "Payback on capex from EBITDA, years", lambda t, c: f"=IF({c}{urow['ebitda']}<=0,\"n/a\",{c}{urow['capex']}/{c}{urow['ebitda']})", DEC)
uline("va_pos", "Memo: to Virgin Active, a bay a year", lambda t, c: f"=-{c}{urow['va']}")
U.cell(urow["debt"], 1).comment = Comment("Instalment on the RMB share of this bay's capex over the amortising term. During the 12-month interest-only period the instalment is lower; see the Debt sheet.", "Model")

# ---------------- Debt ----------------
D = wb.create_sheet("Debt")
D.column_dimensions["A"].width = 10; D.column_dimensions["B"].width = 8
D["A1"] = "RMB facility, monthly, by phase"; D["A1"].font = H1
D["A2"] = "Each phase is drawn in January of its commissioning year, interest-only for the holiday, then amortised over the term. Capex per phase includes any shell cost carried."; D["A2"].font = Font(name=FONT, italic=True)
# phase parameters block rows 4-8, columns C.. per phase (5 cols each)
D.cell(4, 1, "Phase").font = BOLD
labels = ["Capex", "Drawn (RMB share)", "Draw month #", "Monthly instalment after holiday", ""]
pcol = {}
for i in range(3):
    c0 = 3 + i * 6; pcol[i] = c0
    D.cell(4, c0, d["phases"][i]["name"]).font = BOLD
    D.cell(5, c0, "Capex").font = BLACK
    cap = "+".join(f"{ph(i,4+j)}*({bay(t,2)}*{names['fx']}*{names['landed']}+{names['shell']})" for j, t in enumerate(types))
    c = D.cell(5, c0 + 1, f"={cap}"); c.number_format = ZAR; c.font = GREEN
    D.cell(6, c0, "Drawn").font = BLACK
    c = D.cell(6, c0 + 1, f"={L(c0+1)}5*{names['debt_pct']}"); c.number_format = ZAR
    D.cell(7, c0, "Draw month #").font = BLACK
    c = D.cell(7, c0 + 1, f"=({ph(i,2)}-2027)*12+1"); c.number_format = NUM
    D.cell(8, c0, "Instalment").font = BLACK
    c = D.cell(8, c0 + 1, f"={L(c0+1)}6*({names['rate']}/12)/(1-(1+{names['rate']}/12)^-{names['term']})"); c.number_format = ZAR
    for j, h in enumerate(["Opening", "Interest", "Principal", "Closing"]):
        c = D.cell(10, c0 + j, h); c.font = BOLD; c.fill = GREY
    for col in range(c0, c0 + 4): D.column_dimensions[L(col)].width = 15
D.cell(10, 1, "Month #").font = BOLD; D.cell(10, 2, "Year").font = BOLD
D.cell(10, 1).fill = GREY; D.cell(10, 2).fill = GREY
first = 11; nmonths = 72
for m in range(1, nmonths + 1):
    r = first + m - 1
    D.cell(r, 1, m).number_format = NUM
    c = D.cell(r, 2, f"=2027+INT((A{r}-1)/12)"); c.number_format = "0"
    for i in range(3):
        c0 = pcol[i]; O, I, P, C = (L(c0 + k) for k in range(4)); drawn = f"${L(c0+1)}$6"; dm = f"${L(c0+1)}$7"; pmt = f"${L(c0+1)}$8"
        opening = f"=IF(A{r}={dm},{drawn},IF(A{r}>{dm},{C}{r-1},0))" if m > 1 else f"=IF(A{r}={dm},{drawn},0)"
        D.cell(r, c0, opening).number_format = ZAR
        D.cell(r, c0 + 1, f"={O}{r}*{names['rate']}/12").number_format = ZAR
        D.cell(r, c0 + 2, f"=IF(A{r}-{dm}+1>{names['io']},MIN(MAX({pmt}-{I}{r},0),{O}{r}),0)").number_format = ZAR
        D.cell(r, c0 + 3, f"={O}{r}-{P}{r}").number_format = ZAR
last = first + nmonths - 1
# annual summary
sr = last + 3
D.cell(sr, 1, "Annual").font = H2
D.cell(sr + 1, 1, "Year").font = BOLD
for j, y in enumerate(years): c = D.cell(sr + 1, 2 + j, str(y)); c.font = BOLD; c.fill = GREY
drow = {}
lines = [("interest", "Interest", 1), ("principal", "Principal", 2)]
rr = sr + 2
for i in range(3):
    for key, lab, off in lines:
        drow[(i, key)] = rr; D.cell(rr, 1, f"{d['phases'][i]['name']} {lab.lower()}").font = BLACK
        for j, y in enumerate(years):
            col = L(pcol[i] + off)
            c = D.cell(rr, 2 + j, f"=SUMIF($B${first}:$B${last},{y},{col}${first}:{col}${last})"); c.number_format = ZAR
        rr += 1
for key, lab in [("interest", "Total interest"), ("principal", "Total principal"), ("service", "Total debt service"), ("closing", "Closing balance")]:
    drow[key] = rr; D.cell(rr, 1, lab).font = BOLD
    for j, y in enumerate(years):
        col = L(2 + j)
        if key == "service": f = f"={col}{drow['interest']}+{col}{drow['principal']}"
        elif key == "closing": f = "=" + "+".join(f"IF({y}>={ph(i,2)},Debt!${L(pcol[i]+1)}$6,0)" for i in range(3)) + f"-SUMIF($B${first}:$B${last},\"<=\"&{y},$A${first}:$A${last})*0-(" + "+".join(f"SUMIF($B${first}:$B${last},\"<=\"&{y},{L(pcol[i]+2)}${first}:{L(pcol[i]+2)}${last})" for i in range(3)) + ")"
        else: f = "=" + "+".join(f"{col}{drow[(i,key)]}" for i in range(3))
        c = D.cell(rr, 2 + j, f); c.number_format = ZAR; c.font = BOLD
    rr += 1

# ---------------- Chain sheets ----------------
def chain_sheet(title, mult_ref):
    S = wb.create_sheet(title)
    S.column_dimensions["A"].width = 52
    for j in range(len(years)): S.column_dimensions[L(2 + j)].width = 16
    S["A1"] = f"The chain, 2027 to 2032 — {title}"; S["A1"].font = H1
    S["A2"] = "Utilisation multiplier"; c = S["B2"]; c.value = f"={mult_ref}"; c.font = GREEN; c.number_format = DEC
    S.cell(4, 1, "Year").font = BOLD
    for j, y in enumerate(years): c = S.cell(4, 2 + j, str(y)); c.font = BOLD; c.fill = GREY
    rows = {}; r = [5]
    def line(key, label, f, fmt=ZAR, bold=False, top=False, font=None):
        rr = r[0]; rows[key] = rr; S.cell(rr, 1, label).font = BOLD if bold else BLACK
        for j, y in enumerate(years):
            col = L(2 + j)
            c = S.cell(rr, 2 + j, f(y, col, j)); c.number_format = fmt
            c.font = font or (BOLD if bold else BLACK)
            if top: c.border = TOP
        r[0] += 1
    def sub(title):
        r[0] += 1; S.cell(r[0], 1, title).font = H2; r[0] += 1
    for i in range(3):
        sub(d["phases"][i]["name"])
        line(f"age{i}", "Bay age, years", lambda y, col, j, i=i: f"={y}-{ph(i,2)}", NUM)
        line(f"live{i}", "Share of year live", lambda y, col, j, i=i: f"=IF({col}{rows[f'age{i}']}<0,0,IF({col}{rows[f'age{i}']}=0,{ph(i,3)},1))", PCT)
        line(f"f{i}", "Use factor (live × ramp)", lambda y, col, j, i=i: f"={col}{rows[f'live{i}']}*IF({col}{rows[f'age{i}']}=0,{names['ramp0']},IF({col}{rows[f'age{i}']}=1,{names['ramp1']},1))", PCT)
        line(f"capex{i}", "Capex in year", lambda y, col, j, i=i: f"=IF({col}{rows[f'age{i}']}=0,Debt!${L(pcol[i]+1)}$5,0)")
        line(f"bays{i}", "Bays live", lambda y, col, j, i=i: f"=IF({col}{rows[f'age{i}']}>=0,SUM({ph(i,4)}:${L(6)}${phase_rows[i]}),0)", NUM)
        line(f"clubs{i}", "Clubs live", lambda y, col, j, i=i: f"=IF({col}{rows[f'age{i}']}>=0,{ph(i,7)},0)", NUM)
        line(f"hours{i}", "Booked hours", lambda y, col, j, i=i: "=(" + "+".join(f"{ph(i,4+k)}*MIN({bay(t,3)}*$B$2,{names['util_cap']})" for k, t in enumerate(types)) + f")*{names['hours_yr']}*{col}{rows[f'f{i}']}", NUM)
        line(f"hire{i}", "Bay hire", lambda y, col, j, i=i: "=(" + "+".join(f"{ph(i,4+k)}*MIN({bay(t,3)}*$B$2,{names['util_cap']})*{bay(t,4)}" for k, t in enumerate(types)) + f")*{names['hours_yr']}*{col}{rows[f'f{i}']}")
        line(f"memb{i}", "Golf add-on", lambda y, col, j, i=i: f"={ph(i,7)}*{names['members_club']}*{names['adoption']}*$B$2*IF({col}{rows[f'age{i}']}=0,{names['adopt0']},IF({col}{rows[f'age{i}']}=1,{names['adopt1']},1))*{names['addon']}*12*{col}{rows[f'live{i}']}")
        line(f"leagues{i}", "Leagues, events, corporate", lambda y, col, j, i=i: f"={col}{rows[f'bays{i}']}*{names['leagues']}*{col}{rows[f'f{i}']}")
        line(f"chal{i}", "Insured shot, net of premium", lambda y, col, j, i=i: f"={col}{rows[f'hours{i}']}*{names['challenge_hr']}")
        line(f"spons{i}", "Naming partner", lambda y, col, j, i=i: f"={col}{rows[f'bays{i}']}*{names['sponsor']}*{col}{rows[f'live{i}']}")
        line(f"gz{i}", "Golfzon service and software", lambda y, col, j, i=i: "=(" + "+".join(f"{ph(i,4+k)}*{bay(t,2)}*{names['fx']}" for k, t in enumerate(types)) + f")*{names['golfzon']}*{col}{rows[f'live{i}']}")
        line(f"cons{i}", "Consumables and maintenance", lambda y, col, j, i=i: f"={col}{rows[f'bays{i}']}*{names['consumables']}*{col}{rows[f'live{i}']}")
        line(f"ins{i}", "Asset insurance", lambda y, col, j, i=i: f"=Debt!${L(pcol[i]+1)}$5*{names['asset_ins']}*{col}{rows[f'live{i}']}")
    sub("The chain")
    def tot(key): return lambda y, col, j: "=" + "+".join(f"{col}{rows[f'{key}{i}']}" for i in range(3))
    line("bays", "Bays live, total", tot("bays"), NUM, bold=True)
    line("clubs", "Clubs with bays", tot("clubs"), NUM)
    line("hours", "Booked bay-hours", tot("hours"), NUM)
    line("hpd", "Booked hours a bay a day", lambda y, col, j: f"=IF({col}{rows['bays']}=0,0,{col}{rows['hours']}/{col}{rows['bays']}/{names['days']})", DEC)
    line("hire", "Bay hire", tot("hire"))
    line("memb", "Golf add-on memberships", tot("memb"))
    line("leagues", "Leagues, events, corporate", tot("leagues"))
    line("chal", "Get Lucky insured shot, net of premium", tot("chal"))
    line("spons", "Naming partner", tot("spons"))
    line("shared", "Revenue shared with Virgin Active", lambda y, col, j: f"={col}{rows['hire']}+{col}{rows['memb']}+{col}{rows['leagues']}+{col}{rows['chal']}", top=True)
    line("rev", "Revenue", lambda y, col, j: f"={col}{rows['shared']}+{col}{rows['spons']}", bold=True)
    line("va", "Virgin Active concession", lambda y, col, j: f"=-{col}{rows['shared']}*{names['va_share']}")
    line("card", "Card and booking fees", lambda y, col, j: f"=-{col}{rows['shared']}*{names['card']}")
    line("mkt", "Marketing", lambda y, col, j: f"=-{col}{rows['rev']}*{names['marketing']}")
    line("gz", "Golfzon service and software", lambda y, col, j: "=-(" + "+".join(f"{col}{rows[f'gz{i}']}" for i in range(3)) + ")")
    line("cons", "Consumables and maintenance", lambda y, col, j: "=-(" + "+".join(f"{col}{rows[f'cons{i}']}" for i in range(3)) + ")")
    line("ins", "Asset insurance", lambda y, col, j: "=-(" + "+".join(f"{col}{rows[f'ins{i}']}" for i in range(3)) + ")")
    line("people", "People", lambda y, col, j: f"=-Assumptions!{L(2+j)}{people_row}", font=GREEN)
    line("central", "Central overhead", lambda y, col, j: f"=-Assumptions!{L(2+j)}{central_row}", font=GREEN)
    line("ebitda", "EBITDA", lambda y, col, j: f"=SUM({col}{rows['rev']}:{col}{rows['central']})", bold=True, top=True)
    line("margin", "EBITDA margin", lambda y, col, j: f"=IF({col}{rows['rev']}=0,0,{col}{rows['ebitda']}/{col}{rows['rev']})", PCT)
    line("interest", "RMB interest", lambda y, col, j: f"=-Debt!{L(2+j)}{drow['interest']}", font=GREEN)
    line("principal", "RMB capital", lambda y, col, j: f"=-Debt!{L(2+j)}{drow['principal']}", font=GREEN)
    line("service", "Debt service", lambda y, col, j: f"={col}{rows['interest']}+{col}{rows['principal']}", bold=True)
    line("dscr", "Debt cover (EBITDA ÷ debt service)", lambda y, col, j: f"=IF({col}{rows['service']}=0,0,{col}{rows['ebitda']}/-{col}{rows['service']})", X)
    line("cash", "Cash after debt", lambda y, col, j: f"={col}{rows['ebitda']}+{col}{rows['service']}", bold=True, top=True)
    line("capex", "Capex in year", lambda y, col, j: "=" + "+".join(f"{col}{rows[f'capex{i}']}" for i in range(3)))
    line("equity", "Equity deposit (capex not financed by RMB)", lambda y, col, j: f"=-{col}{rows['capex']}*(1-{names['debt_pct']})")
    line("cum", "Cumulative cash after deposits", lambda y, col, j: f"={col}{rows['cash']}+{col}{rows['equity']}" + (f"+{L(1+j)}{rows['cum']}" if j > 0 else ""), bold=True)
    line("va_pos", "Memo: to Virgin Active", lambda y, col, j: f"=-{col}{rows['va']}")
    r[0] += 1
    S.cell(r[0], 1, "Equity needed (lowest point of cumulative cash)").font = BOLD
    c = S.cell(r[0], 2, f"=-MIN(B{rows['cum']}:{L(1+len(years))}{rows['cum']})"); c.number_format = ZAR; c.font = BOLD; c.fill = GREENFILL
    rows["equity_need"] = r[0]
    S.freeze_panes = "B5"
    return rows
base_rows = chain_sheet("Chain", names["mult"])
low_rows = chain_sheet("Chain low", names["mult_low"])
high_rows = chain_sheet("Chain high", names["mult_high"])
wb["Chain"]["A1"] = "The chain, 2027 to 2032 — at the multiplier selected on Assumptions"
wb["Chain low"]["A1"] = "The chain, 2027 to 2032 — low case (fixed at the low multiplier)"
wb["Chain high"]["A1"] = "The chain, 2027 to 2032 — high case (fixed at the high multiplier)"

# ---------------- Summary ----------------
S = wb.create_sheet("Summary", 0)
S.column_dimensions["A"].width = 44
for col in "BCDEFG": S.column_dimensions[col].width = 16
S["A1"] = "Virgin Golf bay model — summary"; S["A1"].font = H1
S["A2"] = "Get Lucky Golf × Virgin Active, financed by RMB. 200 Golfzon bays in 130 clubs. ZAR ex VAT. Change inputs on Assumptions; nothing here is typed in."; S["A2"].font = Font(name=FONT, italic=True)
S["A4"] = "The order"; S["A4"].font = H2
S["A5"] = "Capex, 200 bays landed and installed"; c = S["B5"]; c.value = "=Debt!D5+Debt!J5+Debt!P5"; c.number_format = ZAR; c.font = GREEN
S["A6"] = "RMB facility"; c = S["B6"]; c.value = f"=B5*{names['debt_pct']}"; c.number_format = ZAR
S["A7"] = "Equity deposit"; c = S["B7"]; c.value = "=B5-B6"; c.number_format = ZAR
S["A8"] = "Facility rate"; c = S["B8"]; c.value = f"={names['rate']}"; c.number_format = PCT; c.font = GREEN
S["A10"] = "2031, the first full year at 200 bays"; S["A10"].font = H2
for j, h in enumerate(["Low", "Selected case", "High"]): c = S.cell(11, 2 + j, h); c.font = BOLD; c.fill = GREY
col31 = L(2 + years.index(2031))
def srow(r, label, key, fmt=ZAR, neg=False):
    S.cell(r, 1, label).font = BLACK
    for j, (sheet, rows) in enumerate([("Chain low", low_rows), ("Chain", base_rows), ("Chain high", high_rows)]):
        ref = f"'{sheet}'!{col31}{rows[key]}"
        c = S.cell(r, 2 + j, f"=-{ref}" if neg else f"={ref}"); c.number_format = fmt; c.font = GREEN
srow(12, "Booked hours a bay a day", "hpd", DEC)
srow(13, "Revenue", "rev")
srow(14, "To Virgin Active", "va", neg=True)
srow(15, "EBITDA", "ebitda")
srow(16, "EBITDA margin", "margin", PCT)
srow(17, "Debt service", "service", neg=True)
srow(18, "Debt cover", "dscr", X)
srow(19, "Cash after debt", "cash")
S.cell(20, 1, "Equity needed, deposits and ramp together").font = BOLD
for j, (sheet, rows) in enumerate([("Chain low", low_rows), ("Chain", base_rows), ("Chain high", high_rows)]):
    c = S.cell(20, 2 + j, f"='{sheet}'!B{rows['equity_need']}"); c.number_format = ZAR; c.font = Font(name=FONT, bold=True, color="008000")
S["A22"] = "A bay at maturity, selected case"; S["A22"].font = H2
for j, t in enumerate(types): c = S.cell(23, 2 + j, t); c.font = BOLD; c.fill = GREY
for k, (label, key, fmt) in enumerate([("Landed and installed", "capex", ZAR), ("Booked hours a day", "hpd", DEC), ("Revenue", "rev", ZAR), ("To Virgin Active", "va_pos", ZAR), ("EBITDA", "ebitda", ZAR), ("EBITDA margin", "margin", PCT), ("Payback, years", "payback", DEC)]):
    r = 24 + k; S.cell(r, 1, label).font = BLACK
    for j in range(3):
        c = S.cell(r, 2 + j, f"='Unit economics'!{L(2+j)}{urow[key]}"); c.number_format = fmt; c.font = GREEN

# ---------------- Negotiation ----------------
N = wb.create_sheet("Negotiation")
N.column_dimensions["A"].width = 22; N.column_dimensions["B"].width = 18
for col in "CDEFGHI": N.column_dimensions[col].width = 18
N["A1"] = "The two movable posts — 2031 outcome by Virgin Active's share and who builds the shell"; N["A1"].font = H1
N["A2"] = "Computed from the selected-case chain: a different share moves the concession line; a shell cost carried by Get Lucky Golf moves capex, the RMB instalments, asset insurance and the equity deposit. Debt cover uses 2031 EBITDA over 2031 debt service."; N["A2"].font = Font(name=FONT, italic=True)
hdr = ["Shell built by", "Virgin Active share", "Capex", "To Virgin Active", "Get Lucky Golf EBITDA", "Debt service", "Debt cover", "Equity needed"]
for j, h in enumerate(hdr): c = N.cell(4, 1 + j, h); c.font = BOLD; c.fill = GREY
combos = [("Virgin Active", 0.15), ("Virgin Active", 0.20), ("Virgin Active", 0.25), ("Get Lucky Golf", 0.15), ("Get Lucky Golf", 0.20), ("Get Lucky Golf", 0.25)]
# helper block: per combo per year cumulative cash
N["A14"] = "Helper: cumulative cash after deposits by year, per combination"; N["A14"].font = H2
for j, y in enumerate(years): c = N.cell(15, 3 + j, str(y)); c.font = BOLD; c.fill = GREY
bays_ref = lambda col: "(" + "+".join(f"SUM(Assumptions!$D${phase_rows[i]}:$F${phase_rows[i]})*Chain!{col}{base_rows[f'live{i}']}" for i in range(3)) + ")"
for k, (who, share) in enumerate(combos):
    r = 5 + k
    N.cell(r, 1, who).font = BLACK
    c = N.cell(r, 2, share); c.font = BLUE; c.number_format = PCT
    shell = f"IF($A{r}=\"Get Lucky Golf\",{names['shell_alt']}-{names['shell']},0)"   # extra shell cost per bay versus the selected model
    def ratio(i, rowref):  # each phase's capex, debt and deposit scale by its own bay mix
        sh = shell.replace('$A'+str(r), '$A'+str(rowref))
        return f"(1+{sh}*SUM(Assumptions!$D${phase_rows[i]}:$F${phase_rows[i]})/Debt!${L(pcol[i]+1)}$5)"
    N.cell(r, 3, "=" + "+".join(f"Debt!${L(pcol[i]+1)}$5*{ratio(i, r)}" for i in range(3))).number_format = ZAR
    N.cell(r, 4, f"=Chain!{col31}{base_rows['shared']}*$B{r}").number_format = ZAR
    N.cell(r, 5, f"=Chain!{col31}{base_rows['ebitda']}-($B{r}-{names['va_share']})*Chain!{col31}{base_rows['shared']}-{shell}*{bays_ref(col31)}*{names['asset_ins']}").number_format = ZAR
    N.cell(r, 6, "=" + "+".join(f"(Debt!{col31}{drow[(i,'interest')]}+Debt!{col31}{drow[(i,'principal')]})*{ratio(i, r)}" for i in range(3))).number_format = ZAR
    c = N.cell(r, 7, f"=IF(F{r}=0,0,E{r}/F{r})"); c.number_format = X; c.font = BOLD
    # helper cumulative
    hr = 16 + k
    N.cell(hr, 1, who).font = BLACK; c = N.cell(hr, 2, f"=B{r}"); c.number_format = PCT
    for j, y in enumerate(years):
        col = L(2 + j); hcol = L(3 + j)
        sh = shell.replace('$A'+str(r), '$A'+str(hr))
        ebitda = f"Chain!{col}{base_rows['ebitda']}-($B{hr}-{names['va_share']})*Chain!{col}{base_rows['shared']}-{sh}*{bays_ref(col)}*{names['asset_ins']}"
        service = "-(" + "+".join(f"(Debt!{col}{drow[(i,'interest')]}+Debt!{col}{drow[(i,'principal')]})*{ratio(i, hr)}" for i in range(3)) + ")"
        deposit = "-(" + "+".join(f"Chain!{col}{base_rows[f'capex{i}']}*(1-{names['debt_pct']})*{ratio(i, hr)}" for i in range(3)) + ")"
        prev = f"+{L(2+j)}{hr}" if j > 0 else ""
        c = N.cell(hr, 3 + j, f"=({ebitda}){service}{deposit}{prev}"); c.number_format = ZAR
    c = N.cell(r, 8, f"=-MIN(C{hr}:{L(2+len(years))}{hr})"); c.number_format = ZAR; c.font = BOLD
N.cell(12, 1, "Opening position: 20% and Virgin Active builds the shell. Both posts move to make the deal fit. A bank's usual floor is 1.3× debt cover on the low case; run the selector on Assumptions at 0.7 to see it.").font = Font(name=FONT, size=9, color="595959")

# ---------------- Sources ----------------
R = wb.create_sheet("Sources")
R.column_dimensions["A"].width = 40; R.column_dimensions["B"].width = 110
R["A1"] = "Sources and status of each input"; R["A1"].font = H1
src = [
 ("Virgin Active clubs and members", "136 Southern African clubs, 623,000 members, 35% of group revenue: Virgin Active results to March 2026 as reported by IOL Business Report (13 Nov 2025) and Brait. Collection clubs: virginactive.co.za/memberships."),
 ("Padel pricing", "About R400 an hour, R100 a player in a doubles game: Virgin Active padel pages and virginactivepadelclub.co.za."),
 ("Simulator bay rates in South Africa", "Par 72 Pretoria R210 off-peak to R400 peak a bay-hour; Golf Bar R185 to R370; Golf Sim Centre Cape Town from R150 a person. Sept 2026."),
 ("Golfzon hardware prices", "Golfzon commercial simulators published at $25,000 (TwoVision NX Standard) to $55,000–$90,000 a bay for commercial TwoVision NX (golfzongolf.com; rggolf.com 2026 comparison). Working assumptions until Golfzon quotes in October 2026."),
 ("Golfzon bay footprint", "TwoVision NX: width 16 to 19 ft, length 15 ft 3 in plus 3 ft safety, height 10 ft 2 in minimum (golfzongolf.com plan-your-space). About 5.6 m × 5.5 m × 3.1 m, so a two-bay zone is about 60 m²."),
 ("Golfzon venue guidance", "$50 an hour, 10 booked hours a day, $150,000 to $175,000 a bay a year (golfzongolf.com, start a golf simulator business). The model runs at half the hours and a third of the rate."),
 ("Prime rate", "10.5% (repo 7.0%), effective 28 May 2026, unchanged 23 July 2026. Next MPC 23 September 2026."),
 ("The Point", "Virgin Active's Collection Country Club at Green Point opened 19 February 2026 with a TrackMan simulator (Virgin Active SA build series; launch coverage). Chiswick Riverside in London runs a Trackman iO."),
 ("Insured shot economics", "Stake, prize and 24% premium per the Get Lucky investor model (investgetlucky data/model.json). Santam underwrites."),
 ("Everything else", "Working assumptions by Get Lucky Golf, September 2026: utilisation, yields, add-on take-up, cost lines, RMB margin and structure, landed factor, ramp. Each is an input on Assumptions and is meant to be challenged."),
]
for i, (a, b) in enumerate(src):
    R.cell(3 + i, 1, a).font = BOLD; c = R.cell(3 + i, 2, b); c.alignment = Alignment(wrap_text=True, vertical="top"); c.font = BLACK
    R.row_dimensions[3 + i].height = 45

for ws in wb.worksheets:
    for row_ in ws.iter_rows():
        for c in row_:
            if c.font is None or c.font.name != FONT: c.font = Font(name=FONT, bold=c.font.bold if c.font else False, italic=c.font.italic if c.font else False, color=c.font.color if c.font else None, size=c.font.size if c.font else 10)
wb.save("virgin-golf-bay-model.xlsx")
print("saved")
