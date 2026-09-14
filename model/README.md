# Virgin Golf bay model (Get Lucky Golf x Virgin Active)

Bay economics for the Virgin Active concession and the RMB asset-finance facility.

- `model.py` — every assumption and the calculation. `python3 model.py` prints the three cases and writes `model.json`.
- `build_review.py` — renders `review.html`, the working draft for review, from `model.json`.
- `review.html` — the page. Regenerate, never hand-edit.

Change an assumption in `model.py`, run both scripts, and the page follows.

## The workbook

`build_xlsx.py` writes `virgin-golf-bay-model.xlsx`, the same model as live Excel formulas: Assumptions (blue inputs, a yellow case selector), Unit economics, Chain (selected case), Chain low, Chain high, Debt (monthly, by phase), Negotiation (share × shell grid) and Sources. Every cell is a formula; nothing is typed in. Rebuild after changing `model.py`, then recalculate with LibreOffice and tie out against `model.json`.

## Planet Fitness version
`model_pf.py` is the same engine with Planet Fitness phases: 72 bays in 42 clubs (the 51-club chain less the nine JustGyms), 2027 to 2029, and a cost base sized to 72 bays. Run `python3 model_pf.py` to write `model_pf.json`. The pitch for Planet Fitness is in `planetfitness/`.
