from pathlib import Path
import pandas as pd

data_dir = Path(__file__).parent / "data"

# COLUMNS = [
#     "trip_id",
#     "vendor_id",
#     "pickup_datetime",
#     "dropoff_datetime",
#     "store_and_fwd_flag",
#     "rate_code_id",
#     "pickup_longitude",
#     "pickup_latitude",
#     "dropoff_longitude",
#     "dropoff_latitude",
#     "passenger_count",
#     "trip_distance",
#     "fare_amount",
#     "extra",
#     "mta_tax",
#     "tip_amount",
#     "tolls_amount",
#     "ehail_fee",
#     "improvement_surcharge",
#     "total_amount",
#     "payment_type",
#     "trip_type",
#     "pickup",
#     "dropoff",
#     "cab_type",
#     "precipitation",
#     "snow_depth",
#     "snowfall",
#     "max_temperature",
#     "min_temperature",
#     "average_wind_speed",
#     "pickup_nyct2010_gid",
#     "pickup_ctlabel",
#     "pickup_borocode",
#     "pickup_boroname",
#     "pickup_ct2010",
#     "pickup_boroct2010",
#     "pickup_cdeligibil",
#     "pickup_ntacode",
#     "pickup_ntaname",
#     "pickup_puma",
#     "dropoff_nyct2010_gid",
#     "dropoff_ctlabel",
#     "dropoff_borocode",
#     "dropoff_boroname",
#     "dropoff_ct2010",
#     "dropoff_boroct2010",
#     "dropoff_cdeligibil",
#     "dropoff_ntacode",
#     "dropoff_ntaname",
#     "dropoff_puma",
# ]

df = pd.read_csv(
    data_dir / "decompressed.csv",
    # header=None,
    # names=COLUMNS,
    nrows=50_000,
    low_memory=False,
)

# Convert all object columns to string so Arrow can serialize them
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str)

df.to_csv(data_dir / "decompressed-50k.csv", index=False)

df.to_parquet(data_dir / "decompressed-50k.parquet", index=False)
