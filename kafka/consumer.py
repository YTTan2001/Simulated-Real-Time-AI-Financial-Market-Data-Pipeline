import json
import os
import time
import psycopg2

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from psycopg2 import OperationalError

# Connect to Kafka
while True:
    try:
        consumer = KafkaConsumer(
            "market_data",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="market_consumer_group"
        )

        print("Connected to Kafka")
        break

    except NoBrokersAvailable:
        print("Waiting for Kafka...")
        time.sleep(5)

# Connect to PostgreSQL
while True:
    try:
        conn = psycopg2.connect(
            host="postgres",
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        
        cursor = conn.cursor()

        print("Connected to PostgreSQL")
        break

    except OperationalError as e:
        print(f"Waiting for PostgreSQL... {e}")
        time.sleep(5)

# Consume messages and insert into PostgreSQL
for message in consumer:

    data = message.value

    cursor.execute(
        """
        INSERT INTO market_data (
            trade_date,
            company,
            rd_spending,
            revenue,
            revenue_growth,
            company_event,
            stock_impact
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["trade_date"],
            data["company"],
            data["rd_spending"],
            data["revenue"],
            data["revenue_growth"],
            data["company_event"],
            data["stock_impact"]
        )
    )

    conn.commit()

    print(f"Inserted: {data['company']} ({data['trade_date']})")