import os
import psycopg2
import pandas as pd

def run_quality_check():

    conn = psycopg2.connect(
        host="postgres",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    df = pd.read_sql(
        "SELECT * FROM market_data",
        conn
    )

    if df.empty:
        raise ValueError("No data found")

    bad_records = df[df["revenue"] < 0]

    if not bad_records.empty:
        print(
            f"Found {len(bad_records)} records with negative revenue"
        )
        print("Bad records found:")
        print(bad_records)

    # Keep only valid data
    valid_df = df[df["revenue"] >= 0]

    print(
        f"Valid records: {len(valid_df)}"
    )

    conn.close()

    return valid_df