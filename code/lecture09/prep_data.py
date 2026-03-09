"""ETL script: download NYC yellow taxi CSV and convert to Parquet.

Run once before launching app-02-taxi-dashboard.py:
    python prep_data.py

This script demonstrates the typical ETL prep step:
  raw CSV (large, row-oriented) → Parquet (columnar, compressed, fast)

Source: NYC TLC Trip Record Data (CSV download)
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
"""

from pathlib import Path

import duckdb

# NYC TLC also publishes the same data as CSV (larger, uncompressed)
CSV_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.csv"
OUT = Path(__file__).parent / "data" / "taxi_2024-01.parquet"

OUT.parent.mkdir(exist_ok=True)

print(f"Reading CSV from {CSV_URL} ...")
print("Converting to Parquet (this takes a minute — runs only once) ...")

# read_csv_auto infers headers and column types automatically
duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV_URL}'))
    TO '{OUT}' (FORMAT PARQUET)
""")

size_mb = OUT.stat().st_size / 1e6
print(f"Saved → {OUT}  ({size_mb:.1f} MB)")
print("Parquet is 5-10x faster for filtered queries — DuckDB only reads needed columns.")
print("\nReady. Run: shiny run app-02-taxi-dashboard.py")
