import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.formula.api as smf
    from pathlib import Path
    return Path, mo, np, pd, plt, smf


@app.cell
def _(mo):
    mo.md(
        r"""
        # <Your question, as a title>

        **Question.** <One sentence.>

        **Estimand.** <Population, variable and feature, as in the pre-analysis plan.>

        **Data.** <Source and year; run `uv run python data/get_data.py` first.>

        Every number and figure in the report comes from this notebook. Replace every
        `<...>` and every *TODO*; delete what you do not use.
        """
    )
    return


@app.cell
def _():
    # TODO: the file and the columns of your analysis.
    DATA_FILE = "data/raw/<file>.csv"
    Y = "<outcome>"
    X = "<regressor>"
    W = "<weight>"  # e.g. factor (ENIGH) or fac_tri (ENOE); None if the data have no weights
    CLUSTER = "<psu>"  # e.g. upm; the unit you cluster the standard errors on
    return CLUSTER, DATA_FILE, W, X, Y


@app.cell
def _(DATA_FILE, Path, pd):
    _path = Path(__file__).resolve().parent / DATA_FILE
    if not _path.exists():
        raise FileNotFoundError(f"{_path} not found: run `uv run python data/get_data.py` first.")
    df = pd.read_csv(_path)
    # TODO: the cleaning steps, each one stated (what is dropped and why, how many rows).
    return (df,)


@app.cell
def _(np, pd):
    def wmean(x, w):
        x, w = np.asarray(x, float), np.asarray(w, float)
        return np.sum(w * x) / np.sum(w)

    def wquantile(x, w, q):
        """Quantiles of the weighted ECDF (the plug-in estimate of the population quantiles)."""
        x, w = np.asarray(x, float), np.asarray(w, float)
        order = np.argsort(x)
        x, w = x[order], w[order]
        cdf = np.cumsum(w) / np.sum(w)
        return np.array([x[np.searchsorted(cdf, qq)] for qq in np.atleast_1d(q)])

    def table1(d, y, w, by):
        """Weighted mean, median, P10, P90, n and N-hat of column y by the groups in column by."""
        rows = []
        for g, dd in d.groupby(by):
            xx, ww = dd[y].to_numpy(float), dd[w].to_numpy(float)
            p10, p50, p90 = wquantile(xx, ww, [0.10, 0.50, 0.90])
            rows.append({by: g, "mean": wmean(xx, ww), "median": p50, "P10": p10, "P90": p90,
                         "n": len(dd), "N_hat": ww.sum()})
        return pd.DataFrame(rows).set_index(by)

    return table1, wmean


@app.cell
def _(W, Y, df, table1):
    # TODO: Table 1 by the groups your question compares.
    table1(df, Y, W, by="<group>")
    return


@app.cell
def _(CLUSTER, W, X, Y, df, smf):
    # Weighted or not is your decision; justify it in the plan. Report the other fit as a check.
    _formula = f"{Y} ~ {X}"  # TODO: your specification
    fit = smf.wls(_formula, data=df, weights=df[W]).fit(
        cov_type="cluster", cov_kwds={"groups": df[CLUSTER]}
    )
    fit_unweighted = smf.ols(_formula, data=df).fit(cov_type="HC1")
    fit.summary()
    return fit, fit_unweighted


@app.cell
def _(CLUSTER, W, X, Y, df, np, pd, smf):
    def cluster_bootstrap(d, reps=500, seed=1):
        """Resample whole clusters with replacement and refit; returns the slope draws.
        With a stratified design, resample clusters within each stratum instead."""
        rng = np.random.default_rng(seed)
        groups = dict(tuple(d.groupby(CLUSTER)))
        ids = np.array(list(groups))
        draws = []
        for _ in range(reps):
            sample = pd.concat([groups[i] for i in rng.choice(ids, size=len(ids), replace=True)])
            draws.append(smf.wls(f"{Y} ~ {X}", data=sample, weights=sample[W]).fit().params[X])
        return np.array(draws)

    boot = cluster_bootstrap(df)
    boot_ci = np.percentile(boot, [2.5, 97.5])
    return boot, boot_ci


@app.cell
def _(W, X, Y, df, fit, np, plt, wmean):
    # TODO: the figure that motivates the specification, captioned as an estimator.
    _edges = np.quantile(df[X], np.linspace(0, 1, 21)[1:-1])
    _points = np.array([(wmean(d[X], d[W]), wmean(d[Y], d[W]))
                        for _, d in df.groupby(np.digitize(df[X], _edges))])
    _fig, _ax = plt.subplots(figsize=(6, 4))
    _ax.scatter(_points[:, 0], _points[:, 1], label="weighted means in 20 quantile bins")
    _grid = np.linspace(df[X].min(), df[X].max(), 100)
    _ax.plot(_grid, fit.params["Intercept"] + fit.params[X] * _grid, label="fitted line")
    _ax.set_xlabel(X)
    _ax.set_ylabel(Y)
    _ax.legend()
    _fig
    return


if __name__ == "__main__":
    app.run()
