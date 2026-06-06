import json
import time
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# Load and prepare data
df = pd.read_csv("data/raw/market_data.csv")

df = df.rename(columns={
    "Date": "trade_date",
    "Company": "company",
    "R&D_Spending_USD_Mn": "rd_spending",
    "AI_Revenue_USD_Mn": "revenue",
    "AI_Revenue_Growth_%": "revenue_growth",
    "Event": "company_event",
    "Stock_Impact_%": "stock_impact"
})

df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.strftime("%Y-%m-%d")

# Connect to Kafka
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )
        print("Connected to Kafka")
        break

    except NoBrokersAvailable:
        print("Waiting for Kafka...")
        time.sleep(5)

# Simulate daily streaming
for date in sorted(df["trade_date"].unique()):

    daily_records = (
        df[df["trade_date"] == date]
        .to_dict(orient="records")
    )

    for record in daily_records:
        producer.send("market_data", value=record)  # Kafka topic: market_data

    producer.flush()

    print(f"Sent {len(daily_records)} records for {date}")

    time.sleep(60)  # simulate next trading day

print("All data sent successfully")