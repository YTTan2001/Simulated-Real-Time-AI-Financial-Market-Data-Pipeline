from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, lit, to_date, when, upper, trim
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import os

# Spark Session
spark = (
    SparkSession.builder
    .appName("AI Financial Market Analysis")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("Spark Streaming Started")

# Schema for incoming Kafka data
schema = StructType([
    StructField("trade_date", StringType(), True),
    StructField("company", StringType(), True),
    StructField("rd_spending", DoubleType(), True),
    StructField("revenue", DoubleType(), True),
    StructField("revenue_growth", DoubleType(), True),
    StructField("company_event", StringType(), True),
    StructField("stock_impact", DoubleType(), True)
])

# PostgreSQL Config
jdbc_url = (
    f"jdbc:postgresql://postgres:5432/"
    f"{os.getenv('POSTGRES_DB', 'postgres')}"
)

db_properties = {
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "driver": "org.postgresql.Driver"
}

# Read Kafka Stream
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "market_data")
    .option("startingOffsets", "earliest")
    .load()
)

# Parse JSON and Extract Fields
json_df = kafka_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
)

market_df = (
    json_df
    .select("data.*")
    .withColumn(
        "trade_date",
        to_date(col("trade_date"), "yyyy-MM-dd")
    )
)

# Raw Data
raw_df = market_df

# Clean Data
clean_df = (
    market_df

    # Standardize company names
    .withColumn(
        "company",
        upper(trim(col("company")))
    )

    # Fix event values
    .withColumn(
        "company_event",
        when(
            col("company_event").isin(
                "NaN",
                "\"NaN\"",
                "",
                "null"
            ),
            "NO_EVENT"
        ).otherwise(col("company_event"))
    )

    # Remove invalid records
    .filter(col("revenue") >= 0)
    .filter(col("rd_spending") >= 0)

    # Remove impossible values
    .filter(col("stock_impact").between(-100, 100))
    .filter(col("revenue_growth").between(-500, 500))

    # Remove duplicates
    .dropDuplicates([
        "trade_date",
        "company"
    ])
)

# Write Raw Data
def write_raw(batch_df, batch_id):

    if batch_df.isEmpty():
        return

    print(
        f"Raw Batch {batch_id}: "
        f"{batch_df.count()} rows"
    )

    (
        batch_df.write
        .jdbc(
            url=jdbc_url,
            table="raw_market_data",
            mode="append",
            properties=db_properties
        )
    )
    
# Write Clean Data
def write_clean(batch_df, batch_id):

    if batch_df.isEmpty():
        return

    print(
        f"Clean Batch {batch_id}: "
        f"{batch_df.count()} rows"
    )

    (
        batch_df.write
        .jdbc(
            url=jdbc_url,
            table="clean_market_data",
            mode="append",
            properties=db_properties
        )
    )
    
# Streaming Queries
raw_query = (
    raw_df.writeStream
    .foreachBatch(write_raw)
    .option("checkpointLocation", "/tmp/checkpoints/raw_market_data")
    .outputMode("append")
    .start()
)

clean_query = (
    clean_df.writeStream
    .foreachBatch(write_clean)
    .option("checkpointLocation", "/tmp/checkpoints/clean_market_data")
    .outputMode("append")
    .start()
)

# Monitor Streams
print("Streaming Queries Started")

spark.streams.awaitAnyTermination()