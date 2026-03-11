# https://duckdb.org/2024/10/16/driving-csv-performance-benchmarking-duckdb-with-the-nyc-taxi-dataset

import os
import requests
import gzip
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(script_dir, "files.txt")

output_path = os.path.join(script_dir, "data")

os.makedirs(output_path, exist_ok=True)


def download_data():
    print("Downloading Data:")
    with open(input_file_path, "r") as file:
        urls = file.readlines()
    for url in urls:
        url = url.strip()
        print(url)
        response = requests.get(url.strip(), stream=True)
        response.raise_for_status()
        filename = os.path.join(output_path, url.split("/")[-1])
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


COLUMNS = [
    "trip_id", "vendor_id", "pickup_datetime", "dropoff_datetime",
    "store_and_fwd_flag", "rate_code_id", "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude", "passenger_count", "trip_distance",
    "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount", "ehail_fee",
    "improvement_surcharge", "total_amount", "payment_type", "trip_type",
    "pickup", "dropoff", "cab_type", "precipitation", "snow_depth", "snowfall",
    "max_temperature", "min_temperature", "average_wind_speed",
    "pickup_nyct2010_gid", "pickup_ctlabel", "pickup_borocode", "pickup_boroname",
    "pickup_ct2010", "pickup_boroct2010", "pickup_cdeligibil", "pickup_ntacode",
    "pickup_ntaname", "pickup_puma",
    "dropoff_nyct2010_gid", "dropoff_ctlabel", "dropoff_borocode", "dropoff_boroname",
    "dropoff_ct2010", "dropoff_boroct2010", "dropoff_cdeligibil", "dropoff_ntacode",
    "dropoff_ntaname", "dropoff_puma",
]


def prepare_data():
    output_file = os.path.join(output_path, "decompressed.csv")
    header = ",".join(COLUMNS) + "\n"
    with open(output_file, "wb") as f:
        f.write(header.encode())
    for filename in os.listdir(output_path):
        if filename.endswith(".csv.gz"):
            gz_file_path = os.path.join(output_path, filename)
            with gzip.open(gz_file_path, "rb") as gz_file:
                with open(output_file, "ab") as out_file:
                    shutil.copyfileobj(gz_file, out_file)
            print(f"Decompressed: {gz_file_path}")


download_data()
prepare_data()
