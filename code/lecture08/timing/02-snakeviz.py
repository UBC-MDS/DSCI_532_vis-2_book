import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Profiling with cProfile + snakeviz
    """)
    return


@app.cell
def _():
    import cProfile
    from pathlib import Path
    import pandas as pd
    import ibis

    data_dir = Path(__file__).parent / "data"
    csv_path = data_dir / "decompressed-50k.csv"
    parquet_path = data_dir / "decompressed-50k.parquet"
    prof_path_parquet = data_dir / "profile-pandas-parquet.prof"
    prof_path_csv = data_dir / "profile-pandas-csv.prof"
    prof_path_ibis = data_dir / "profile-ibis.prof"
    return (
        cProfile,
        csv_path,
        ibis,
        parquet_path,
        pd,
        prof_path_csv,
        prof_path_ibis,
        prof_path_parquet,
    )


@app.cell
def _(mo):
    mo.md("""
    ## pandas — parquet
    """)
    return


@app.cell
def _(cProfile, parquet_path, pd, prof_path_parquet):
    def analyze_trips_parquet():
        df = pd.read_parquet(parquet_path)
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
        df["hour"] = df["pickup_datetime"].dt.hour
        return (
            df.groupby(["cab_type", "hour"])
            .agg(
                mean_fare=("fare_amount", "mean"),
                total_revenue=("total_amount", "sum"),
                trip_count=("trip_id", "count"),
            )
            .reset_index()
            .sort_values(["cab_type", "hour"])
        )

    cProfile.run("analyze_trips_parquet()", str(prof_path_parquet))
    prof_path_parquet
    return


@app.cell
def _(mo, prof_path_parquet):
    mo.md(f"""
    ```bash\nsnakeviz {prof_path_parquet}\n```
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## pandas — csv
    """)
    return


@app.cell
def _(cProfile, csv_path, pd, prof_path_csv):
    def analyze_trips_csv():
        df = pd.read_csv(csv_path)
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
        df["hour"] = df["pickup_datetime"].dt.hour
        return (
            df.groupby(["cab_type", "hour"])
            .agg(
                mean_fare=("fare_amount", "mean"),
                total_revenue=("total_amount", "sum"),
                trip_count=("trip_id", "count"),
            )
            .reset_index()
            .sort_values(["cab_type", "hour"])
        )

    cProfile.run("analyze_trips_csv()", str(prof_path_csv))
    prof_path_csv
    return


@app.cell
def _(mo, prof_path_csv):
    mo.md(f"""
    ```bash\nsnakeviz {prof_path_csv}\n```
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## ibis — duckdb backend
    """)
    return


@app.cell
def _(cProfile, ibis, parquet_path, prof_path_ibis):
    def analyze_trips_ibis():
        t = ibis.read_parquet(str(parquet_path))
        t = t.mutate(hour=t.pickup_datetime.cast("timestamp").hour())
        return (
            t.group_by(["cab_type", "hour"])
            .agg(
                mean_fare=t.fare_amount.mean(),
                total_revenue=t.total_amount.sum(),
                trip_count=t.trip_id.count(),
            )
            .order_by(["cab_type", "hour"])
            .execute()
        )

    cProfile.run("analyze_trips_ibis()", str(prof_path_ibis))
    prof_path_ibis
    return


@app.cell
def _(mo, prof_path_ibis):
    mo.md(f"""
    ```bash\nsnakeviz {prof_path_ibis}\n```
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
