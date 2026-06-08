import os
import psycopg2
import pandas as pd

def run_anomaly_detection():

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

    mean = df["stock_impact"].mean()
    std = df["stock_impact"].std()

    df["z_score"] = (
        df["stock_impact"] - mean
    ) / std

    anomalies = df[
        abs(df["z_score"]) > 3
    ]

    cursor = conn.cursor()

    for _, row in anomalies.iterrows():

        cursor.execute(
            """
            INSERT INTO anomaly_results
            (
                trade_date,
                company,
                stock_impact,
                z_score,
                anomaly_flag
            )
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                row["trade_date"],
                row["company"],
                row["stock_impact"],
                row["z_score"],
                True
            )
        )

    conn.commit()

    print(
        f"Detected {len(anomalies)} anomalies"
    )

    conn.close()