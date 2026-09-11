"""Get Lucky Golf x Virgin Active (the Virgin Golf concept) - bay economics for the Virgin Active concession
and the RMB asset-finance facility. Run: python3 model.py  -> writes model.json
All money in ZAR ex VAT. FX 18.5 (same as the Get Lucky investor model).
"""
import json

FX = 18.5
PRIME = 0.105            # SA prime, Sept 2026
RATE = PRIME + 0.015     # RMB asset finance, prime + 1.5%
IO_M = 12                # interest-only while a phase is commissioned and ramps
TERM_M = 60              # then 5-year amortising, per phase drawdown
DEBT_PCT = 0.90          # RMB funds 90% of landed capex; Get Lucky Golf equity 10%
LANDED = 1.30            # freight, duty, enclosure, screen, seating, install on top of hardware
HOURS_PER_BAY = 15 * 360 # bookable hours a year (05:00-21:00 weekdays, shorter weekends)
VA_SHARE = 0.20          # Virgin Active concession: 20% of bay revenue. Opening position, negotiable
SHELL_PER_BAY = 150_000  # room shell and power if Get Lucky Golf builds it instead of Virgin Active. Opening position: Virgin Active builds
CARD = 0.025             # card and booking fees
MARKETING = 0.05         # of revenue
ASSET_INS = 0.01         # of capex, a year
GOLFZON_SVC = 0.04       # software, courses, service contract: % of hardware a year
CONSUMABLES = 24_000     # per bay a year
LEAGUES_PER_BAY = 40_000 # leagues, events, corporate, at maturity
SPONSOR_PER_BAY = 25_000 # naming partner, per bay a year
CHALLENGE_PER_HOUR = 31 * 0.76  # Get Lucky insured shot: R50, 0.625 taken per booked hour, net of 24% premium
MEMBERS_PER_CLUB = 623_000 / 136
ADDON_ZAR_PM = 299       # golf membership add-on on the Virgin Active bill, ex VAT
ADDON_ADOPTION = 0.015   # of members at clubs with bays, at maturity
DEPR_YEARS = 7
TAX = 0.27

BAYS = {  # hardware USD, mature utilisation, blended yield per booked hour (ZAR)
    "Signature": dict(hw_usd=60_000, util=0.40, yld=520, label="TwoVision NX, Collection and flagship clubs"),
    "Play":      dict(hw_usd=35_000, util=0.33, yld=360, label="Vision Standard, metro clubs"),
    "Practice":  dict(hw_usd=22_000, util=0.30, yld=240, label="GDR Plus, coaching bays"),
}
for b in BAYS.values():
    b["hw"] = b["hw_usd"] * FX
    b["capex"] = b["hw"] * LANDED

# phases: (year commissioned, fraction of that year live, {type: units}, clubs)
PHASES = [
    dict(name="Phase 1", year=2027, live=0.50, units={"Signature": 40}, clubs=20),   # two Signature bays a club
    dict(name="Phase 2", year=2028, live=0.50, units={"Play": 100}, clubs=50),       # two Play bays a club
    dict(name="Phase 3", year=2029, live=0.60, units={"Play": 20, "Practice": 40}, clubs=60),  # one bay a club
]
RAMP = {0: 0.55, 1: 0.80}  # of mature, by bay age in years; 2+ = 1.0
def ramp(age): return RAMP.get(age, 1.0)

def annuity(p, r_m, n):
    return p * r_m / (1 - (1 + r_m) ** -n)

def debt_schedule(principal, start_year, years):
    """Annual interest and principal for a 60-month amortiser drawn at start of commissioning year."""
    r = RATE / 12
    pmt = annuity(principal, r, TERM_M)
    bal = principal; month = 0
    out = {y: dict(interest=0.0, principal=0.0, closing=0.0) for y in years}
    for y in years:
        for _ in range(12):
            if y < start_year or bal <= 1e-6: continue
            month += 1
            i = bal * r
            pr = 0.0 if month <= IO_M else min(pmt - i, bal)
            bal -= pr
            out[y]["interest"] += i; out[y]["principal"] += pr
        out[y]["closing"] = bal
    return out, pmt

def run(util_mult=1.0, va_share=VA_SHARE, shell=0.0):
    years = list(range(2027, 2033))
    rows = {}
    capex_by_phase = []
    for ph in PHASES:
        cap = sum((BAYS[t]["capex"] + shell) * n for t, n in ph["units"].items())
        capex_by_phase.append(cap)
    total_capex = sum(capex_by_phase)
    debts = [debt_schedule(c * DEBT_PCT, ph["year"], years) for c, ph in zip(capex_by_phase, PHASES)]

    for y in years:
        r = dict(year=y, bays=0, clubs=0, hours=0.0, bay_hire=0.0, membership=0.0, leagues=0.0,
                 challenge=0.0, sponsorship=0.0, golfzon=0.0, consumables=0.0, asset_ins=0.0, capex=0.0)
        for ph, cap in zip(PHASES, capex_by_phase):
            age = y - ph["year"]
            if age < 0: continue
            live = ph["live"] if age == 0 else 1.0
            f = live * ramp(age)
            if age == 0: r["capex"] += cap
            r["bays"] += sum(ph["units"].values()); r["clubs"] += ph["clubs"]
            for t, n in ph["units"].items():
                b = BAYS[t]
                hrs = n * HOURS_PER_BAY * min(b["util"] * util_mult, 0.85) * f
                r["hours"] += hrs
                r["bay_hire"] += hrs * b["yld"]
                r["challenge"] += hrs * CHALLENGE_PER_HOUR
                r["leagues"] += n * LEAGUES_PER_BAY * f
                r["sponsorship"] += n * SPONSOR_PER_BAY * live
                r["golfzon"] += n * b["hw"] * GOLFZON_SVC * live
                r["consumables"] += n * CONSUMABLES * live
                r["asset_ins"] += cap * ASSET_INS * live / sum(ph["units"].values()) * n
            members = ph["clubs"] * MEMBERS_PER_CLUB
            adoption = ADDON_ADOPTION * util_mult * {0: 0.4, 1: 0.75}.get(age, 1.0)
            r["membership"] += members * adoption * ADDON_ZAR_PM * 12 * live
        shared = r["bay_hire"] + r["membership"] + r["leagues"] + r["challenge"]
        r["revenue"] = shared + r["sponsorship"]
        r["va_share"] = shared * va_share
        r["card"] = shared * CARD
        r["marketing"] = r["revenue"] * MARKETING
        # people: hosts at Collection clubs, regional technicians, a small central team
        r["people"] = {2027: 4.0e6, 2028: 8.0e6, 2029: 11.0e6}.get(y, 12.0e6)
        r["central"] = {2027: 2.0e6, 2028: 3.0e6}.get(y, 4.0e6)
        r["opex"] = sum(r[k] for k in ("va_share", "card", "marketing", "golfzon", "consumables", "asset_ins", "people", "central"))
        r["ebitda"] = r["revenue"] - r["opex"]
        r["interest"] = sum(d[0][y]["interest"] for d in debts)
        r["principal"] = sum(d[0][y]["principal"] for d in debts)
        r["debt_service"] = r["interest"] + r["principal"]
        r["debt_closing"] = sum(d[0][y]["closing"] for d in debts)
        r["dscr"] = r["ebitda"] / r["debt_service"] if r["debt_service"] else None
        r["cash_after_debt"] = r["ebitda"] - r["debt_service"]
        rows[y] = r
    # cumulative
    cum = 0.0; equity = 0.0
    for y in years:
        r = rows[y]
        equity += r["capex"] * (1 - DEBT_PCT)
        cum += r["cash_after_debt"] - r["capex"] * (1 - DEBT_PCT)
        r["equity_in"] = r["capex"] * (1 - DEBT_PCT); r["cum_cash"] = cum
    return dict(years=years, rows=rows, total_capex=total_capex, capex_by_phase=capex_by_phase,
                debt_total=total_capex * DEBT_PCT, equity_total=total_capex * (1 - DEBT_PCT),
                pmt_monthly=[d[1] for d in debts])

def negotiation():
    """2031 outcome for each combination of Virgin Active's share and who builds the shell."""
    grid = []
    for shell_by, shell in (("Virgin Active", 0.0), ("Get Lucky Golf", SHELL_PER_BAY)):
        for share in (0.15, 0.20, 0.25):
            R = run(1.0, share, shell); r = R["rows"][2031]
            trough = min(R["rows"][y]["cum_cash"] for y in R["years"])
            grid.append(dict(shell_by=shell_by, share=share, capex=R["total_capex"], debt=R["debt_total"],
                             va_income=r["va_share"], ebitda=r["ebitda"], debt_service=r["debt_service"],
                             dscr=r["dscr"], cash_after_debt=r["cash_after_debt"], equity_need=-trough,
                             dscr_low=run(0.7, share, shell)["rows"][2031]["dscr"]))
    return grid

def unit_econ(t, util_mult=1.0):
    b = BAYS[t]
    hrs = HOURS_PER_BAY * b["util"] * util_mult
    bay_hire = hrs * b["yld"]; challenge = hrs * CHALLENGE_PER_HOUR
    leagues = LEAGUES_PER_BAY; sponsor = SPONSOR_PER_BAY
    # membership allocated per bay: chain-level membership at maturity / 200 bays
    clubs = sum(p["clubs"] for p in PHASES); bays = sum(sum(p["units"].values()) for p in PHASES)
    membership = clubs * MEMBERS_PER_CLUB * ADDON_ADOPTION * util_mult * ADDON_ZAR_PM * 12 / bays
    shared = bay_hire + challenge + leagues + membership
    revenue = shared + sponsor
    costs = dict(va_share=shared * VA_SHARE, card=shared * CARD, marketing=revenue * MARKETING,
                 golfzon=b["hw"] * GOLFZON_SVC, consumables=CONSUMABLES, asset_ins=b["capex"] * ASSET_INS,
                 people_central=16.0e6 / bays)
    ebitda = revenue - sum(costs.values())
    debt = annuity(b["capex"] * DEBT_PCT, RATE / 12, TERM_M) * 12  # full amortising year
    return dict(type=t, label=b["label"], hw_usd=b["hw_usd"], capex=b["capex"], hours=hrs, util=b["util"] * util_mult,
                yld=b["yld"], bay_hire=bay_hire, membership=membership, leagues=leagues, challenge=challenge,
                sponsorship=sponsor, revenue=revenue, costs=costs, ebitda=ebitda, margin=ebitda / revenue,
                debt_service=debt, cash_after_debt=ebitda - debt, payback_years=b["capex"] / ebitda,
                va_share=costs["va_share"])

if __name__ == "__main__":
    cases = {"low": 0.70, "base": 1.00, "high": 1.25}
    out = dict(fx=FX, prime=PRIME, rate=RATE, term_months=TERM_M, io_months=IO_M, debt_pct=DEBT_PCT, landed=LANDED,
               hours_per_bay=HOURS_PER_BAY, va_share=VA_SHARE, addon_zar_pm=ADDON_ZAR_PM, addon_adoption=ADDON_ADOPTION,
               members_per_club=MEMBERS_PER_CLUB, bays=BAYS, phases=PHASES,
               cases={k: run(v) for k, v in cases.items()},
               unit={t: unit_econ(t) for t in BAYS}, unit_low={t: unit_econ(t, 0.7) for t in BAYS},
               shell_per_bay=SHELL_PER_BAY, negotiation=negotiation())
    json.dump(out, open("model.json", "w"), indent=1, default=float)
    m = lambda x: f"R{x/1e6:6.1f}m"
    for case, mult in cases.items():
        R = run(mult)
        print(f"\n=== {case.upper()} (utilisation x{mult}) capex {m(R['total_capex'])} debt {m(R['debt_total'])} equity {m(R['equity_total'])}")
        print(f"{'year':>6}{'bays':>6}{'hrs/bay/d':>10}{'revenue':>10}{'VA share':>10}{'EBITDA':>10}{'margin':>8}{'debt svc':>10}{'DSCR':>6}{'cash':>10}{'cum':>10}")
        for y in R["years"]:
            r = R["rows"][y]
            hpd = r["hours"] / r["bays"] / 360 if r["bays"] else 0
            print(f"{y:>6}{r['bays']:>6}{hpd:>10.1f}{m(r['revenue']):>10}{m(r['va_share']):>10}{m(r['ebitda']):>10}{r['ebitda']/r['revenue']*100 if r['revenue'] else 0:>7.0f}%{m(r['debt_service']):>10}{(r['dscr'] or 0):>6.2f}{m(r['cash_after_debt']):>10}{m(r['cum_cash']):>10}")
    print("\n=== NEGOTIATION GRID, 2031")
    for g in negotiation():
        print(f"shell by {g['shell_by']:>13}, VA {g['share']*100:.0f}%: capex {m(g['capex'])} VA income {m(g['va_income'])} EBITDA {m(g['ebitda'])} DSCR {g['dscr']:.2f} (low {g['dscr_low']:.2f}) equity {m(g['equity_need'])}")
    print("\n=== UNIT ECONOMICS, mature bay, base case")
    for t in BAYS:
        u = unit_econ(t)
        print(f"{t:>10}: capex {m(u['capex'])} hrs/day {u['hours']/360:4.1f} rev {m(u['revenue'])} (hire {m(u['bay_hire'])} memb {m(u['membership'])}) VA {m(u['va_share'])} EBITDA {m(u['ebitda'])} {u['margin']*100:.0f}% debt {m(u['debt_service'])} payback {u['payback_years']:.1f}y")
