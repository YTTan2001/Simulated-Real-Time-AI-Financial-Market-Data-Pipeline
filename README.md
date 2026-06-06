# AI Financial Market Analysis (Phase 1)
## Project Description
Phase 1 focuses on building a real-time financial market data ingestion pipeline. Historical market data stored in a CSV file is streamed to simulate real-time market activity. The objective of this phase is to establish a scalable and reliable data pipeline for collecting and storing financial data, without performing any data analysis or visualization.

## Technologies Used
### Apache Kafka
Apache Kafka serves as the real-time streaming platform for the project.
- *Kafka Producer* reads market data from a CSV file and publishes records at fixed intervals to simulate live market feeds.
- *Kafka Broker* manages message delivery through Kafka topics.
- *Kafka Consumer* subscribes to topics and processes incoming market data for downstream storage.

### PostgreSQL
PostgreSQL is used as the centralized database for storing raw financial market data received from Kafka.
- Stores historical and streamed market records.
- Provides a structured foundation for future analysis and reporting phases.

### Docker
Docker containerizes all project components to ensure:
- Consistent development and deployment environments.
- Easy setup and execution across different machines.
- Simplified dependency management.

## Project Workflow
CSV Market Data
       │
       ▼
Kafka Producer
       │
       ▼
Kafka Topic (market_data)
       │
       ▼
Kafka Consumer
       │
       ▼
PostgreSQL Database

## Future Enhancements (Phase 2)
- Near real-time data processing/ data quality check (orchestrated by Apache Airflow)
- Anomalies detection (orchestrated by Apache Airflow)

## Key Learning Outcomes
- Building event-driven data pipelines using Apache Kafka.
- Simulating real-time data streams from historical datasets.
- Integrating Kafka with PostgreSQL for persistent storage.
- Containerizing distributed systems with Docker.
- Designing scalable architectures for financial data processing.

## Appendix
![alt text](Images/image.png)
_Daily data loaded into postgresSQL database successfully with 1 min interval_

![alt text](Images/image-2.png)
![alt text](Images/image-1.png)
_Postgres database that store real-time raw market data_
