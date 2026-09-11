# Virgin Golf bay model (Get Lucky Golf x Virgin Active)

Bay economics for the Virgin Active concession and the RMB asset-finance facility.

- `model.py` — every assumption and the calculation. `python3 model.py` prints the three cases and writes `model.json`.
- `build_review.py` — renders `review.html`, the working draft for review, from `model.json`.
- `review.html` — the page. Regenerate, never hand-edit.

Change an assumption in `model.py`, run both scripts, and the page follows.

## The workbook

`build_xlsx.py` writes `virgin-golf-bay-model.xlsx`, the same model as live Excel formulas: Assumptions (blue inputs, a yellow case selector), Unit economics, Chain (selected case), Chain low, Chain high, Debt (monthly, by phase), Negotiation (share × shell grid) and Sources. Every cell is a formula; nothing is typed in. Rebuild after changing `model.py`, then recalculate with LibreOffice and tie out against `model.json`.
