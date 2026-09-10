# Legal research — the insured hole-in-one challenge on simulators

**Get Lucky Golf Club (Pty) Ltd · Registration 2025/047585/07 · compiled 10 September 2026**

## Purpose and status

This document is the company's own legal research on the simulator product. It is **not legal
advice and no lawyer has reviewed it.** It exists so that, when we engage counsel, they start
from an organised brief rather than a blank page: the product as the law will see it, the
precedent we have found, the tests each jurisdiction applies, what comparable products already
do, our working state tiers, the structures that change the answer, and the specific questions
we need answered. Every conclusion here is a working position for counsel to confirm or overturn.

| Item | Status |
|---|---|
| Counsel engaged | **Not yet.** To be engaged before any pilot term sheet is signed (STRATEGY.md, gate G3) |
| South Africa | Written skill-based opinion held (on-course product); simulator variant not yet opined on |
| United States | Research complete (this document, Parts A–C); opinion outstanding |
| South Korea | Research notes only (Part D); Korean counsel outstanding; phase-two market |
| UK / EU | Notes only (Part D); per-country opinion outstanding |

## Brief for counsel — the questions we need answered

1. **Characterisation.** Is a $1-per-attempt, insurer-funded, fixed-prize hole-in-one challenge
   on a simulator a contest of skill rather than gambling, under (a) the predominant-factor test,
   (b) a material-element statute (NY PL 225.00, NJ 2C:37-1, RCW 9.46.0225), and (c) a
   wager-focused statute? What weight do *Las Vegas Hacienda*, *Cobaugh*, *Chenard*, *Grove* and
   Florida AGO 90-58 carry today?
2. **The 18 Green states.** Confirm paid entry with our official rules, 18+ age gate, venue
   geolocation and 1099 reporting is lawful in each, and list any state-specific disclosure or
   rules requirements (e.g. California B&P §§ 17539.1–17539.3).
3. **The comparables' exclusions.** Why do Skill Strike and Five Iron exclude NV, PA, WA, NH and
   VA, and does the reason apply to a fixed, insurer-funded prize?
4. **Structure B.** Confirm that operator- or sponsor-funded free play (no consideration from the
   golfer) carries no gambling exposure in any state, and identify any prize-promotion
   registration, bonding or disclosure it triggers (FL, NY, RI thresholds; AZ; others).
5. **Structure E.** Whether bundling the insured swing into the bay rate at no increment removes
   consideration in Arizona-type states.
6. **Funds flow and licensing.** Any state requiring a licence or registration for the entry-fee
   collector, the prize-indemnity insurer (admitted carrier / surplus lines / Lloyd's coverholder)
   or the payment processor; merchant-category and UIGEA considerations for the acquiring bank.
7. **Operator contract.** Allocation of compliance responsibility between Get Lucky and the
   operator (Golfzon Tour puts it on the host facility); indemnities; the data-sharing clause for
   ace rate by handicap band.
8. **South Korea (phase two).** Whether an insurance-wrapped product (golfer as policyholder, a
   Korean carrier, Golfzon as distributor, Santam Re behind) avoids Criminal Act §246 and the
   Speculative Acts law, and what distribution licence the operator needs.
9. **The $1,000 → $1,000,000 tier.** Does a four-figure entry change the characterisation in any Green state (consumer-protection, responsible-play or licensing thresholds keyed to stake size); what KYC/AML, tax withholding and reporting attach to a $1M skill-contest prize; and whether a handicap-tiered prize (different prize for the same entry by verified ability) raises any fairness or disclosure issue.
10. **UK / EU.** Whether the product is a prize competition with a genuine skill element outside
   the Gambling Act 2005 (s.14), and the equivalent per EU country of launch.

Documents we will provide counsel: the official rules draft; the prize-indemnity policy schedule
(Santam via Indwe) and the fund-flow diagram; the app spec's verification and geo-gating sections
(`GetLucky_App_Requirements.md` §24, P-12); the existing South African opinion; pilot telemetry
(ace rate by handicap band, by hole) as soon as a pilot is live.

---

# Part A — United States: the concept, the precedent, the tests

The working brief for the US gaming-law opinion (STRATEGY.md action 5): the concept as a lawyer
will see it, the precedent directly on point, the tests each state applies, what the three live
real-money simulator products already exclude, and a working tier for every state.

## 1. The concept, as the law sees it

| Element | The product | Why it matters |
|---|---|---|
| **Prize** | An insured cash prize ($500 at 500×; $1,000 at 1,000×) for holing a par-3 tee shot on a simulator | Present in every state's definition of gambling |
| **Consideration** | $1 (or $2/$5) entry per qualifying hole, paid to Get Lucky inside the operator's app | Present — unless the operator or a sponsor funds it (see §6) |
| **Chance** | A single tee shot; the golfer's own performance; the simulator measures the result | The whole case turns on whether skill "predominates" (or, in stricter states, whether chance is a "material element" or present "to any degree") |
| **Who funds the prize** | Santam (or a US carrier) under a prize-indemnity policy — never the entry fees, never a pool | Decisive in Florida-type states: an entry fee that does not make up the prize is not a "stake, bet or wager" |
| **Who competes** | Only the golfer, against a fixed target. Get Lucky and the operator never compete for the prize | The sponsor not competing is the second limb of the Florida test |
| **Where** | A physical bay in a licensed venue, geolocated by venue | Jurisdiction is unambiguous — an advantage over mobile skill apps |

Three features distinguish this from every US comparable: the prize is **insurer-funded and fixed**
(not a pool of entries, not a house edge), the contest is **the golfer against the hole** (not
against other players, not against the house), and the fee is **small and per attempt**.

## 2. Precedent directly on point

| Case / opinion | Facts | Holding | Why it matters to us |
|---|---|---|---|
| **Las Vegas Hacienda, Inc. v. Gibson**, 77 Nev. 25, 359 P.2d 85 (Nev. 1961) | Public offer: pay **50 cents** for the chance to win **$5,000** by shooting a hole-in-one on the resort's course. Golfer aced; resort refused to pay | Not a gaming transaction; contract enforceable. Expert evidence that "a skilled player will get it in the area where luck will take over more often than an unskilled player" was sufficient to sustain a finding that a hole-in-one is a **feat of skill** | This is our product — a small fee, a large fixed prize, one swing — and the leading case says it is skill, not gambling |
| **Florida AGO 90-58** (Attorney General, 1990), with AGO 66-41 | "Whether a contest of skill, such as a hole-in-one golf contest, where contestants pay an entry fee, which does not directly make up the prize… violates the gambling laws" | "**Does not violate the gambling laws of this state.**" The fee is not a "stake, bet or wager" where the prize is paid from the sponsor's general assets and the sponsor does not compete. But s. 849.14 is violated where entry fees make up the pot | An insurer-funded fixed prize is the cleanest possible version of the structure the AG approved. Pooled-entry products (Five Iron Tournaments, NEXT) sit on the wrong side of this line in Florida — ours does not |
| **Cobaugh v. Klick-Lewis, Inc.**, 385 Pa. Super. 587, 561 A.2d 1248 (Pa. Super. 1989) | Car offered for an ace at the 9th; golfer paid a tournament entry fee, aced, dealer refused | Enforced as a unilateral contract. "There was no evidence in this case that an element of chance was the dominant factor in shooting the hole-in-one"; pros are roughly twice as likely as amateurs to ace, so skill is not "almost an irrelevant factor" | The majority applied the **dominant-factor** test to a single-shot ace and found for skill. **Judge Popovich's dissent** is the best-articulated counter-argument in US law: aces are "such a fortuitous event that skill is almost an irrelevant factor" — expect opposing counsel or a regulator to quote it |
| **Chenard v. Marcel Motors**, 387 A.2d 596 (Me. 1978) | Elks Lodge tournament; dealer donated a Dodge Colt for an ace; golfer aced | Enforced | Maine court treated an ace prize as an enforceable contract, not an illegal wager |
| **Grove v. Charbonneau Buick-Pontiac, Inc.**, 240 N.W.2d 853 (N.D. 1976) | Car for "the first entry who shoots a hole-in-one on Hole No. 8"; 18 holes played on a 9-hole course | Enforced | North Dakota — a state with a consideration rule for promotions — enforced an ace prize in a paid-entry tournament |
| National Hole-in-One Registry (cited in GOLF.com, 2026) | Per-shot odds: Tour player 3,000:1; low handicapper 5,000:1; average player 12,000:1 | — | A **4× skill differential** between the best and average golfers is the evidence that skill predominates. Golfzon's 2022 network rate of 1 in 6,992 sits between the two |

The pattern across every reported case: courts enforce hole-in-one prizes as contracts and, when
asked, find that skill predominates. No reported US case has held a paid-entry hole-in-one contest
to be illegal gambling. The risk is not the case law; it is the handful of states whose statutes
do not ask the skill question at all.

## 3. The four tests, and which states use them

| Test | What it asks | States (working list — courts are not always consistent) | Effect on us |
|---|---|---|---|
| **Predominant (dominant) factor** — the "American rule" | Does skill account for more than half of the outcome? | The majority: CA (In re Allen, 1962), NC (Joker Club, 2007), IL (Dew-Becker v. Wu, 2020), NY (White v. Cuomo, 2022 — despite "material degree" statutory wording), GA, OH, MI (courts), PA (Cobaugh), FL (AGO 90-58), MA, WI, MN, VA (courts), and most others | Our case is strongest here; Hacienda and Cobaugh are dominant-factor decisions |
| **Material element** | Is chance present to a material degree, even if skill dominates? | Statutory wording in NY (PL 225.00), NJ (2C:37-1), WA (RCW 9.46.0225), plus (per Cabot et al., 57 Drake L. Rev. 383) AL, AK, HI, MO, OK, OR — though NY has resolved to dominant factor and AL/AK lean that way | Harder: a single-shot ace has an obvious chance component. Needs the skill-differential evidence and, ideally, a no-consideration structure |
| **Any chance** | Does any element of chance exist? | TX case law (State v. Gambling Device, 1993 — though the Penal Code carves out bona fide skill contests), TN by statute ("to any degree contingent on chance", § 39-17-501), AR, historically SD | Paid entry is not defensible under a literal any-chance test. Free/operator-funded only |
| **Wager-focused (no skill question)** | Was money risked on the outcome of *any* game? | LA (R.S. 14:90 — "risks the loss of anything of value in order to realize a profit", no chance element); SC (§ 16-19-40; 2025 decision: "even skill games with entry fees are prohibited"); MD; MI statute (MCL 750.303: "allowing gambling on games of skill or chance is prohibited", per the MGCB bulletin); MT (§ 23-5-112); SD (§ 22-25-1) | Paid entry is out regardless of how skilful the shot is |

Two further overlays:
- **Consideration rules for promotions.** Maryland (Com. Law § 13-305), Nebraska, North Dakota and Colorado are cited by promotion-law practitioners as prohibiting consideration for a contest; Vermont repealed its rule in 2013 (9 V.S.A. § 2481x now allows entry fees for games of skill).
- **"Bona fide contest" carve-outs.** Illinois (720 ILCS 5/28-1(b)(2)), Texas (Penal Code § 47.01(1)(B)) and Georgia define "bet"/"gambling" to *exclude* "an offer of a prize, award or compensation to the actual contestants in a bona fide contest for the determination of skill, speed, strength or endurance". A hole-in-one challenge is a contest of skill between the golfer and the hole; counsel should confirm a single-attempt format is "bona fide".

## 4. What the live comparables exclude (as at Sep 2026)

| Product | Structure | States excluded | Source |
|---|---|---|---|
| **Full Swing Skill Strike** (Evenplay) | Per-shot closest-to-pin wagering, house-edge, skill-adjusted | **AK, HI, MD, NV, NH, VA** — "legal in 44 states" | fullswinggolf.com/full-swing-skill-strike; PR Newswire launch release |
| **Five Iron Tournaments** (Lucra wallet) | Pooled-entry tournaments and $1 CTP with guaranteed pools; 21+ | **CT, DE, NV, PA, WA** ("including but not limited to"); 15 markets in 11 states + DC at launch | fiveirongolf.com/terms-and-conditions |
| **Skillz** (mobile skill games) | Head-to-head cash matches | **AR, CT, DE, LA, SD** (2022 terms); older developer docs also list AZ, MT, SC, TN; IN and ME card games only | skillz.com/legal; docs.skillz.com |
| **Players' Lounge** (esports) | Head-to-head cash | AZ, AR, CT, DE, **FL**, IN, LA, MD, MT, SC, SD, TN | playerslounge.com/support |
| **Golfzon Tour** | Team stroke play, $300k purse | "Void where prohibited"; host facility responsible | golfzontour.com/rules-and-regulations |

Read together: the consensus "never" list is **AR, CT, DE, LA, SD, MT, SC, TN, AZ, MD**; the
"depends on structure/regulator" list is **NV, PA, WA, NH, VA, AK, HI, IN, FL**. Note Florida:
Players' Lounge excludes it because pooled entries fund the prize (s. 849.14); AGO 90-58 says a
fixed sponsor-funded prize is fine — which is exactly why our insured prize is better placed in
Florida than Five Iron's.

# Part B — State-by-state working tiers

## 5. The tiers

**Tier key.** 🟢 **Green** — paid $1 entry with standard official rules, age 18+, venue geolocation
and 1099 reporting; counsel confirms, no structural change expected. 🟡 **Amber** — counsel opinion
before paid launch; likely workable with the evidence package (§7) or a structural tweak; launch
free-to-play first. 🔴 **Red** — no paid entry; operator- or sponsor-funded free-to-play only (§6),
or skip.

| State | Test / key law | Specific issues | Comparables | Tier |
|---|---|---|---|---|
| Alabama | Dominant factor in practice (Op. of the Justices, 2001); constitutional lottery ban; listed as material-element by some commentators | Conservative enforcement culture | Skillz live | 🟡 |
| Alaska | Material element (Morrow v. State, 1973) | Skill Strike excludes | Excluded by Skill Strike | 🟡 |
| Arizona | § 13-3301 "amusement gambling": skill games may only award **merchandise** prizes (wholesale value capped); the "athletic event" exception requires that no one other than the players profits from the money paid | Cash prize for a paid skill game does not fit any exception; Get Lucky and the operator profit from entries | Historically excluded by Skillz; excluded by Players' Lounge | 🔴 |
| Arkansas | Statute reaches betting on "any game of hazard or skill"; any-chance heritage | — | Excluded by Skillz | 🔴 |
| California | Dominant factor (In re Allen, 1962); B&P Code §§ 17539.1–17539.3 regulate skill contests that charge fees (disclosures, no chance in later rounds) | Compliance-heavy but permissive; official rules must meet § 17539.1 | Skillz, Skill Strike live | 🟢 |
| Colorado | Gambling defined as risk "contingent in whole **or in part** upon… chance"; promotion practitioners list CO as prohibiting consideration in contests | Statute wording + consideration rule | Skillz live | 🟡 |
| Connecticut | § 53-278a "gambling" = risking money on a contest of chance or future contingent event not under one's control; restrictive AG posture on cash skill contests | — | Excluded by Skillz, Five Iron, Players' Lounge | 🔴 |
| Delaware | Broad anti-gambling statutes reaching any game; constitutional lottery ban | — | Excluded by Skillz, Five Iron, Players' Lounge | 🔴 |
| District of Columbia | Dominant factor; DFS legal | — | Five Iron live | 🟢 |
| Florida | AGO 90-58: hole-in-one contest with an entry fee that does not fund the prize is **not** gambling; s. 849.14 bars wagering on contests of skill where fees make the pot or the sponsor competes | Structure must keep fees out of the prize — ours does by design (insurer pays) | Five Iron live (FL venues); Players' Lounge excludes (pooled) | 🟢 |
| Georgia | Dominant factor; "bet" excludes prizes to actual contestants in a bona fide skill contest | — | Five Iron live (Atlanta) | 🟢 |
| Hawaii | All gambling prohibited; material element | No real-money skill products operate | Excluded by Skill Strike | 🔴 |
| Idaho | Broad constitutional ban; DFS not permitted | — | — | 🟡 |
| Illinois | Dominant factor (Dew-Becker v. Wu, 2020); 720 ILCS 5/28-1(b)(2) exempts prizes to actual contestants in a bona fide skill contest | — | Five Iron live (Chicago) | 🟢 |
| Indiana | Skillz restricts card games only; Players' Lounge excludes; Five Iron live (Indianapolis) | Mixed signals — likely fine for an athletic skill contest | Five Iron live | 🟡 |
| Iowa | Restrictive contest/gambling code (ch. 725; "bona fide contest" exemptions narrow) | — | Skillz live | 🟡 |
| Kansas | Dominant factor | — | — | 🟢 |
| Kentucky | Dominant factor; loss-recovery statute; DFS legal | — | Five Iron live (KY venues) | 🟢 |
| Louisiana | R.S. 14:90 — gambling is risking anything of value "in order to realize a profit" in any game or contest; **no chance element** | Paid entry is gambling by definition | Excluded by Skillz, Players' Lounge | 🔴 |
| Maine | Dominant factor; Chenard enforced an ace prize | Skillz restricts card games only | — | 🟢 |
| Maryland | Com. Law § 13-305 prohibits consideration for a contest; gambling law focuses on the wager, not skill (Ifrah) | — | Excluded by Skill Strike, Players' Lounge | 🔴 |
| Massachusetts | Dominant factor; DFS regulated by AG | — | Five Iron live (Boston) | 🟢 |
| Michigan | Courts use dominant factor, but MCL 750.303 bars "allowing gambling on games of skill or chance" and the MGCB bulletin says so plainly; Ifrah lists MI as wager-focused | Five Iron operates in Detroit — check whether paid or free-only there | Five Iron (Detroit) | 🟡 |
| Minnesota | Dominant factor; DFS not authorised | — | — | 🟡 |
| Mississippi | Broad prohibition outside licensed casinos | — | Skillz social-casino exclusion | 🟡 |
| Missouri | Material element (Thole v. Westfall, 1984) | — | Skillz live | 🟡 |
| Montana | § 23-5-112 "gambling activity" reaches games or contests generally | — | Excluded by Skillz (historic), Players' Lounge | 🔴 |
| Nebraska | Consideration prohibited for contests (promotion practitioners); "any chance" heritage | — | — | 🟡 |
| Nevada | Hacienda (1961) is our best case — but NRS 463 now regulates contests and tournaments, entry fees and promotions in association with gaming; regulators' reach has grown | Both Skill Strike and Five Iron exclude NV; expect Gaming Control Board engagement | Excluded by Skill Strike, Five Iron | 🟡 |
| New Hampshire | Skill Strike excludes | Reason not established in public sources | Excluded by Skill Strike | 🟡 |
| New Jersey | 2C:37-1 material element (Boardwalk Regency, 1982: backgammon is gambling); DFS legal by statute | Statutory wording is the issue; Skillz operates (bar dominoes) | Skillz live | 🟡 |
| New Mexico | Dominant factor | — | — | 🟢 |
| New York | PL 225.00 "material degree" wording, but White v. Cuomo (2022) applied dominant factor; DFS statute | Five Iron is headquartered and live in NYC | Five Iron live | 🟢 |
| North Carolina | Dominant factor (Joker Club, 2007) | — | — | 🟢 |
| North Dakota | Consideration prohibited for contests (promotion practitioners) — yet Grove enforced an ace prize | — | — | 🟡 |
| Ohio | Dominant factor | — | Five Iron live (OH venues) | 🟢 |
| Oklahoma | Material element (per Cabot) | — | — | 🟡 |
| Oregon | Material element (State v. Coats lineage); DFS not permitted | — | — | 🟡 |
| Pennsylvania | Cobaugh (1989) is for us; but In re: Three PA Skill Amusement (Pa. 15 Jun 2026) held "skill game" devices are slot machines under the Gaming Act, and Five Iron excludes PA | Device-based ruling, not a sports contest — but the climate is hostile to "skill" framing | Excluded by Five Iron | 🟡 |
| Rhode Island | Dominant factor; registration for retail games of chance only | — | — | 🟢 |
| South Carolina | § 16-19-40; 2025 decision: "even skill games with entry fees are prohibited" (Ifrah) | — | Excluded by Skillz (historic), Players' Lounge | 🔴 |
| South Dakota | § 22-25-1 gambling "in any form… wherein anything valuable is wagered upon the outcome" | — | Excluded by Skillz, Players' Lounge | 🔴 |
| Tennessee | § 39-17-501: "risking anything of value for a profit whose return is **to any degree contingent on chance**"; AG opined DFS illegal before the statute (2016) | Any-chance by statute | Excluded by Skillz (historic), Players' Lounge | 🔴 |
| Texas | Penal Code § 47.01(1)(B): "bet" excludes prizes to actual contestants in a bona fide skill contest; but case law reads devices under an any-chance lens | Carve-out is strong for an athletic contest | — | 🟢 |
| Utah | Constitutional ban on gambling; statute keyed to "element of chance" | — | — | 🟡 |
| Vermont | 9 V.S.A. § 2481x allows entry fees for games of skill (since 2013) | — | — | 🟢 |
| Virginia | 2020 "skill games" ban (devices); § 18.2-325 "illegal gambling" = any bet or wager on the outcome of a game or contest; Skill Strike excludes | Statute is wager-focused | Excluded by Skill Strike | 🔴 |
| Washington | RCW 9.46.0225 material degree; Gambling Commission active; Five Iron excludes WA (though it lists Seattle venues) | — | Excluded by Five Iron; Skill Strike live | 🟡 |
| West Virginia | Broad statute | — | — | 🟡 |
| Wisconsin | Dominant factor | — | — | 🟢 |
| Wyoming | Dominant factor | — | — | 🟢 |

**Counts:** 🟢 18 (CA, DC, FL, GA, IL, KS, KY, ME, MA, NM, NY, NC, OH, RI, TX, VT, WI, WY) ·
🟡 21 · 🔴 12 (AR, AZ, CT, DE, HI, LA, MD, MT, SC, SD, TN, VA).

The Green list contains the pilot geography that matters: **New York, Florida, Illinois, Georgia,
Massachusetts, Ohio, Kentucky, DC** — every Five Iron launch market except Detroit, Seattle and
Las Vegas — plus **California and Texas**, where Golfzon reports its fastest US growth. Virginia
being Red is awkward only symbolically: Golfzon America's office is in Fairfax County, but no
venue there needs to run paid entry for the deal to work.

# Part C — Structures, evidence and the federal overlay

## 6. Structures that change the answer

| Structure | Consideration? | Where it unlocks | Cost |
|---|---|---|---|
| **A. Paid entry, insurer-funded prize** (the product) | Yes | Green states now; Amber with an opinion | — |
| **B. Operator-funded free play** — the venue or a sponsor pays Get Lucky per bay per month; the golfer pays nothing extra for the insured swing | **No** — the gambling analysis falls away; only prize-promotion rules apply (official rules; FL/NY registration only if a *chance*-based prize exceeds $5,000 — ours does not) | Red and Amber states; also the natural launch format for a Golfzon or Topgolf "house" promotion | Get Lucky's revenue becomes a B2B licence fee (46% of a notional $1 → a per-bay rate), not a per-entry share |
| **C. Sponsor-funded** — an insurer or brand sponsors the prize (the Santam model) and the golfer plays free | No | Same as B; strongest in markets where a territory sponsor is part of the plan anyway | Sponsorship revenue instead of entries |
| **D. Membership-included swing** — one insured swing a month inside a paid Golfzon/Five Iron membership | Yes (membership is consideration) | Does not change the analysis; treat as A | — |
| **E. Bundled with bay time** — the insured swing is included in the hourly bay rate with no increment | Arguable: Arizona's "intellectual contest" exception and several states' promotion rules treat a purchase at the normal price as non-consideration | Possible route in AZ-type states; counsel to test | Operator absorbs the cost |

Recommendation for the pilot: **A in Green states, B in every other state from day one** — the
same slip, the same bay, the only difference being who pays the dollar. That gives a nationwide
footprint for an operator like Golfzon without a state-by-state launch gate, and B is the format a
Topgolf or a Golfzon Social will want for its own promotions anyway.

## 7. The evidence package for counsel (what will win the skill argument)

1. **Skill differential by ability.** Ace rates by handicap band from the pilot telemetry
   (Golfzon and Five Iron both hold this): if a 5-handicap aces 3–5× more often than a 20, skill
   predominates on the Cobaugh reasoning. The Registry's 3,000:1 vs 12,000:1 is the public
   version; sim data will be sharper because the target is fixed.
2. **Repeated attempts at a fixed target.** GOLF.com's own point: hitting shot after shot at the
   same familiar target in simulated conditions is a very different thing from a par-3 you have
   never seen — the repeatability is what makes it skill. The **designated Get Lucky hole** — one
   fixed par-3 per course, chosen by Get Lucky and built into the operator's software, never by
   the player — makes the target fixed and the per-hole ace rate measurable, which is the evidence
   base for the skill argument and for the insurer's rate card.
3. **The prize is not the pool.** Insurance certificate, policy schedule and the fund flow diagram
   (entry → Get Lucky/operator; claim → insurer → winner). This is the Florida AGO 90-58 structure.
4. **No house edge, no counterparty.** Get Lucky's economics do not improve when the golfer misses
   by more; the operator does not compete; nobody bets on anyone else.
5. **Operational controls.** Age 18+ (21+ where the venue serves alcohol and prefers it, as Five
   Iron does), venue geolocation, one entry per hole per round, locked simulator settings,
   telemetry verification, KYC on payout, 1099-MISC for prizes of $600+, self-exclusion and
   entry limits in the app.

## 8. Federal overlay (brief)

- **UIGEA** (31 U.S.C. § 5361 et seq.): a "bet or wager" is money staked on "a contest of others, a
  sporting event, or a game subject to chance". A golfer's own performance in a skill contest is
  none of those; payment processing for a physical in-venue activity is not "unlawful internet
  gambling". Confirm with counsel and the acquiring bank (merchant category matters).
- **Wire Act**: sports betting only. **IGBA**: depends on state law — hence the state tiers.
- **Tax**: prizes are ordinary income to the winner; 1099-MISC at $600+, not W-2G.
- **Prize indemnity**: a regulated insurance line. The insured is Get Lucky (or the operator); a
  US-admitted carrier or a Lloyd's coverholder is needed for US risks if Santam does not front.

## 9. What this changes in the strategy (US)

- The **US pilot is Green-state only** for paid entry: New York and Florida first (Five Iron NYC;
  Golfzon Social NY; Ernie's Florida), then Illinois, Georgia, Massachusetts, Ohio, Texas, California.
- **Structure B (operator-funded free play) ships in the same release** so Golfzon can switch the
  slip on nationwide and no state is a launch blocker.
- **The opinion request to counsel** is now specific: confirm the 18 Green states for Structure A
  with our official rules; advise on NY/NJ/WA material-element wording; advise on the five
  "comparables exclude" states (NV, PA, WA, NH, VA); confirm Structure B carries no gambling
  exposure anywhere and identify any prize-promotion registration it triggers.
- **Ask both pilot partners for ace rate by handicap band** in the data-sharing clause — it is
  the single most persuasive piece of evidence on the skill question.

# Part D — Other markets (research notes, no counsel yet)

## 10. South Africa

The on-course product operates as a competition with an operator-funded, insured prize: an entry
fee to Get Lucky, a prize paid by the insurer, no pot and no counterparty. The company holds a
written legal opinion that this is skill-based and requires no gaming licence. The simulator
variant changes the verifier (machine telemetry instead of a camera) and the venue (a bay, not a
tee); it does not change the fund flow. **Ask:** a short supplementary opinion covering the
simulator variant, the free side games (modelled at zero revenue precisely because South Africa's
informal-bet exemption dies the moment a third party takes a gain) and the membership-included
swing. Underwriter: Santam, Authorised FSP 3416; broker of record: Indwe.

## 11. South Korea (phase two)

- **Criminal Act Article 246** prohibits gambling; the Supreme Court has held that golf betting
  games are gambling even though skill affects the outcome (Korea Times, 27 Oct 2008;
  Chambers Gaming Law 2025, South Korea).
- **Act on Special Cases concerning Regulation and Punishment of Speculative Acts**
  (사행행위 등 규제 및 처벌 특례법) defines a speculative act as collecting money from many people and
  deciding gain or loss by chance, and lists "현상업" — awarding property to those who achieve a
  specified thing — among permit-only businesses. A paid-entry ace prize could be read as 현상업.
- **Game Industry Promotion Act** bans cash prizes in game venues, but screen-golf centres have
  been ruled athletic facilities, not game venues (Golf Digest; PMC review).
- **What demonstrably works:** insurance. Carrot × Golfzon (2020), Lotte CREW (Jan 2026) and NH
  all sell the golfer a short-term hole-in-one policy at the bay, with Golfzon transmitting the
  ace video to the insurer. **Working structure for Korea:** the golfer is the policyholder, a
  Korean carrier underwrites, Golfzon distributes as an insurance agent, Santam Re sits behind
  the carrier. Fraud is a known problem in Korean ace insurance (staged aces; an agent's licence
  revoked) — telemetry verification is a selling point to a Korean carrier.
- **Ask Korean counsel:** whether the insurance wrapper avoids §246 and 현상업; the distribution
  licence Golfzon needs; whether a fixed "congratulation money" sum (as 골프단짝 pays) is treated as
  insurance or as a prize; advertising rules for insurance sold at a sports facility.

## 12. United Kingdom and EU

- **UK:** a prize competition sits outside the Gambling Act 2005 where success depends on the
  exercise of skill, judgement or knowledge that would deter a significant proportion of entrants
  or prevent a significant proportion from winning (s.14). A single-shot ace will be argued both
  ways; the same skill-differential evidence applies. Five Iron operates in London; NEXT Golf
  Tour runs paid entries from Denmark. UK prize-indemnity brokers (Lloyd's coverholders) serve
  events, so capacity exists.
- **EU:** gambling is regulated nationally; each launch country needs its own opinion. Denmark
  (NEXT's home) and the Netherlands (Solheim Cup 2026, Trackman) are the natural first questions.
- **Ask:** a UK opinion on s.14 for the paid product and on the free-play structure; a
  short per-country memo for any EU pilot market before launch.

## Sources

- Las Vegas Hacienda, Inc. v. Gibson, 77 Nev. 25, 359 P.2d 85 (1961) — https://law.justia.com/cases/nevada/supreme-court/1961/4319-1.html
- Cobaugh v. Klick-Lewis, Inc., 385 Pa. Super. 587, 561 A.2d 1248 (1989) — https://law.justia.com/cases/pennsylvania/supreme-court/1989/385-pa-super-587-1.html (majority and Popovich dissent)
- Chenard v. Marcel Motors, 387 A.2d 596 (Me. 1978) — https://law.justia.com/cases/maine/supreme-court/1978/387-a-2d-596-0.html
- Grove v. Charbonneau Buick-Pontiac, Inc., 240 N.W.2d 853 (N.D. 1976) — https://law.justia.com/cases/north-dakota/supreme-court/1976/9180-2.html
- Florida AGO 90-58, "Gambling, games of skill" — https://www.myfloridalegal.com/ag-opinions/gambling-games-of-skill ; Fla. Stat. § 849.14 — https://www.flsenate.gov/laws/statutes/2025/849.14
- Tests: Ifrah Law, "Enforcement of Gambling Laws Against Skill Games in Outlier States" — https://www.ifrahlaw.com/ifrah-on-igaming/gambling-on-skill-enforcement-of-gambling-laws-against-skill-games-in-outlier-states/ ; Harwood, "Better Good Than Lucky", Wash. U. L. Rev. (2024) — https://wustllawreview.org/2024/07/01/better-good-than-lucky-a-legal-analysis-of-poker-as-a-skill-game-in-a-changing-gambling-climate/ ; Cabot, Light & Rutledge, 57 Drake L. Rev. 383 (2009); Holland & Knight (2022) — https://www.hklaw.com/en/insights/publications/2022/05/marketers-beware-your-social-media-sweepstakes-or-contests-could-be
- Statutes: Ariz. Rev. Stat. § 13-3301 (amusement gambling) — https://www.azleg.gov/ars/13/03301.htm ; La. R.S. 14:90 — https://www.legis.la.gov/legis/Law.aspx?d=78698 ; Tenn. Code § 39-17-501 — https://law.justia.com/codes/tennessee/title-39/chapter-17/part-5/section-39-17-501/ and Tenn. AG Op. 16-013 ; RCW 9.46.0225/.0237 — https://app.leg.wa.gov/rcw/default.aspx?cite=9.46 ; 720 ILCS 5/28-1 — https://www.ilga.gov/documents/legislation/ilcs/documents/072000050K28-1.htm ; Md. Com. Law § 13-305 ; MGCB Bulletin on Illegal Gaming — https://www.michigan.gov/mgcb/-/media/Project/Websites/mgcb/Home-Page-Resources/Bulletin_on_Illegal_Gaming_745572_7.pdf ; S.C. Code § 16-19-40 ; Va. Code § 18.2-325 — https://law.lis.virginia.gov/vacodefull/title18.2/chapter8/article1/ ; NRS ch. 463 — https://www.leg.state.nv.us/nrs/nrs-463.html ; 9 V.S.A. § 2481x (Vermont) — Loeb & Loeb 2013 note ; N.Y. Penal Law § 225.00 ; N.J.S.A. 2C:37-1
- Pennsylvania: In re: Three PA Skill Amusement (Pa. 15 Jun 2026) — https://law.justia.com/cases/pennsylvania/supreme-court/2026/50-map-2024.html ; Saiber note 16 Jun 2026
- Virginia skill-games ban — Fairfax County handout (Oct 2024) — https://www.fairfaxcounty.gov/legislation/sites/legislation/files/Assets/documents/pdf/2024/Skill-Games-Ban-for-Businesses-Handout-for-10.15.24.pdf ; VPM 21 Apr 2026
- Comparables: Full Swing Skill Strike — https://www.fullswinggolf.com/full-swing-skill-strike/ and PR Newswire launch release; Five Iron Golf Terms & Conditions — https://fiveirongolf.com/terms-and-conditions ; Skillz Legal — https://www.skillz.com/legal/ and https://docs.skillz.com/docs/28.0.18/legal-skillz/ ; Players' Lounge restricted locations — https://www.playerslounge.com/support/restricted-locations ; Golfzon Tour rules — https://www.golfzontour.com/rules-and-regulations
- Consideration rules: Enns & Archer — https://www.ennsandarcher.com/s_basics.html ; Realtime Media — https://www.rtm.com/blog/contests-and-sweepstakes-laws-by-state ; Fasthoff Law — https://fasthofflawfirm.com/blog/skill-contests-versus-sweepstakes-entry-fees ; registration/bonding (FL, NY, RI) — Raven5 — https://raven5.com/contest-and-sweepstakes-registration-and-bonding-requirements/
- Ace odds: GOLF.com, "The odds of making a golf-simulator hole in one? We mined the data" — https://golf.com/news/odds-making-golf-simulator-hole-in-one/
