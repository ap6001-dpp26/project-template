# <Your question, as a title>

AP6001 *Probabilidad y estadística* · final project · <your name>

## Question

<One sentence, and two or three on why it matters for policy.>

## Estimand

<The population, the variable and the feature (conditional mean, difference in means, BLP slope,
quantile), as a formula and in one sentence of words.>

## Data

<Source, year, unit of observation. How to obtain it: `data/get_data.py`, or the exact steps if it
cannot be scripted. The design (strata, primary sampling units, weights) or, for a census or
administrative records, the coverage.>

## Reproduce

```bash
uv sync                          # installs the packages pinned in uv.lock
uv run python data/get_data.py   # downloads the data into data/raw/
uv run python notebook.py        # runs the analysis; or: uv run marimo edit notebook.py
```

## Contents

| Path | What it is |
|---|---|
| `data/get_data.py` | Downloads the raw data (not committed) |
| `notebook.py` | marimo notebook: every number and figure in the report |
| `report/` | The report source and the rendered PDF |
