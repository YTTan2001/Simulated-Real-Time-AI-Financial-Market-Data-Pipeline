import os
import pandas as pd
from sqlalchemy import create_engine

def run_anomaly_detection():

    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}"
        f"@postgres:5432/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    # Get latest processed anomaly date

    try:

        latest = pd.read_sql(
            """
            SELECT
                COALESCE(
                    MAX(trade_date),
                    '2015-01-01'
                ) AS last_date
            FROM anomaly_results
            """,
            engine
        )

        last_date = latest.iloc[0]["last_date"]

    except Exception:

        last_date = "2015-01-01"

    # Load market data

    df = pd.read_sql(
        """
        SELECT *
        FROM clean_market_data
        ORDER BY company, trade_date
        """,
        engine
    )

    if len(df) < 30:
        
        print("Not enough records")

        engine.dispose()

        return 0

    df["trade_date"] = pd.to_datetime(
        df["trade_date"]
    )

    # Rolling statistics

    df["rolling_mean"] = (
        df.groupby("company")["stock_impact"]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(
                 window=30,
                 min_periods=10
            )
            .mean()
        )
    )

    df["rolling_std"] = (
        df.groupby("company")["stock_impact"]
        .transform(
            lambda x:
            x.shift(1)
            .rolling(
                window=30,
                min_periods=10
            )
            .std()
        )
    )

    df["z_score"] = (
        (
            df["stock_impact"]
            -
            df["rolling_mean"]
        )
        /
        df["rolling_std"]
    )


    # Detect anomalies

    anomalies = df[
        df["z_score"].abs() > 3
    ].copy()

    anomalies["anomaly_flag"] = True

    # Only process new anomalies

    anomalies = anomalies[
        anomalies["trade_date"] > pd.to_datetime(last_date)
    ]

    if len(anomalies) == 0:

        print("No new anomalies")

        engine.dispose()

        return 0

# --------------------------------------------------
# Remove duplicates
# --------------------------------------------------

    try:

        existing = pd.read_sql(
            """
            SELECT
                trade_date,
                company
            FROM anomaly_results
            """,
            engine
        )

        anomalies = anomalies.merge(
            existing,
            on=[
                "trade_date",
                "company"
            ],
            how="left",
            indicator=True
        )

        anomalies = anomalies[
            anomalies["_merge"] == "left_only"
        ].drop(
            columns="_merge"
        )

    except Exception:
        pass

    if len(anomalies) == 0:

        print("No unique anomalies")

        engine.dispose()

        return 0

# --------------------------------------------------
# Save results
# --------------------------------------------------

    anomalies[
        [
            "trade_date",
            "company",
            "stock_impact",
            "z_score",
            "anomaly_flag"
        ]
    ].to_sql(
        "anomaly_results",
        engine,
        if_exists="append",
        index=False
    )

    anomaly_count = len(anomalies)

    print(
        f"{anomaly_count} anomalies detected"
    )

    engine.dispose()

    return anomaly_count
