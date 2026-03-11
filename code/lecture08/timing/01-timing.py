import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import time
    from pathlib import Path
    import pandas as pd
    import polars as pl
    import ibis
    import duckdb

    data_dir = Path(__file__).parent / "data"
    csv_path = data_dir / "decompressed-50k.csv"
    parquet_path = data_dir / "decompressed-50k.parquet"
    return csv_path, duckdb, ibis, parquet_path, pd, pl, time


@app.cell
def _(mo):
    mo.md("""
    # I/O + groupby timing: CSV vs Parquet across frameworks
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(csv_path, pd, time):
    _t0 = time.perf_counter()
    _df = pd.read_csv(csv_path)
    _result = _df.groupby("cab_type")["total_amount"].mean()
    pandas_csv_time = time.perf_counter() - _t0
    pandas_csv_time
    return (pandas_csv_time,)


@app.cell
def _(parquet_path, pd, time):
    _t0 = time.perf_counter()
    _df = pd.read_parquet(parquet_path)
    _result = _df.groupby("cab_type")["total_amount"].mean()
    pandas_parquet_time = time.perf_counter() - _t0
    pandas_parquet_time
    return (pandas_parquet_time,)


@app.cell
def _(csv_path, pl, time):
    _t0 = time.perf_counter()
    _df = pl.read_csv(csv_path)
    _result = _df.group_by("cab_type").agg(pl.col("total_amount").mean())
    polars_csv_time = time.perf_counter() - _t0
    polars_csv_time
    return (polars_csv_time,)


@app.cell
def _(parquet_path, pl, time):
    _t0 = time.perf_counter()
    _df = pl.read_parquet(parquet_path)
    _result = _df.group_by("cab_type").agg(pl.col("total_amount").mean())
    polars_parquet_time = time.perf_counter() - _t0
    polars_parquet_time
    return (polars_parquet_time,)


@app.cell
def _(csv_path, ibis, time):
    _t0 = time.perf_counter()
    _t = ibis.read_csv(str(csv_path))
    _result = _t.group_by("cab_type").agg(mean_fare=_t.total_amount.mean()).execute()
    ibis_csv_time = time.perf_counter() - _t0
    ibis_csv_time
    return (ibis_csv_time,)


@app.cell
def _(ibis, parquet_path, time):
    _t0 = time.perf_counter()
    _t = ibis.read_parquet(str(parquet_path))
    _result = _t.group_by("cab_type").agg(mean_fare=_t.total_amount.mean()).execute()
    ibis_parquet_time = time.perf_counter() - _t0
    ibis_parquet_time
    return (ibis_parquet_time,)


@app.cell
def _(csv_path, duckdb, time):
    _t0 = time.perf_counter()
    _con = duckdb.connect()
    _result = _con.execute(
        f"SELECT cab_type, AVG(total_amount) FROM read_csv_auto('{csv_path}') GROUP BY cab_type"
    ).df()
    duckdb_csv_time = time.perf_counter() - _t0
    duckdb_csv_time
    return (duckdb_csv_time,)


@app.cell
def _(duckdb, parquet_path, time):
    _t0 = time.perf_counter()
    _con = duckdb.connect()
    _result = _con.execute(
        f"SELECT cab_type, AVG(total_amount) FROM read_parquet('{parquet_path}') GROUP BY cab_type"
    ).df()
    duckdb_parquet_time = time.perf_counter() - _t0
    duckdb_parquet_time
    return (duckdb_parquet_time,)


@app.cell
def _(
    duckdb_csv_time,
    duckdb_parquet_time,
    ibis_csv_time,
    ibis_parquet_time,
    mo,
    pandas_csv_time,
    pandas_parquet_time,
    pd,
    polars_csv_time,
    polars_parquet_time,
):
    summary = pd.DataFrame({
        "framework": ["pandas", "pandas", "polars", "polars", "ibis", "ibis", "duckdb", "duckdb"],
        "format": ["csv", "parquet", "csv", "parquet", "csv", "parquet", "csv", "parquet"],
        "time_s": [
            pandas_csv_time, pandas_parquet_time,
            polars_csv_time, polars_parquet_time,
            ibis_csv_time, ibis_parquet_time,
            duckdb_csv_time, duckdb_parquet_time,
        ],
    }).round(3)
    mo.ui.table(summary)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
