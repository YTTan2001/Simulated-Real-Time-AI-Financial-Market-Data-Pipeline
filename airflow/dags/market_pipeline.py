from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

from scripts.data_quality_check import run_quality_check
from scripts.anomaly_detection import run_anomaly_detection

with DAG(
    dag_id="market_pipeline",
    start_date=datetime(2015, 1, 1),
    schedule="*/1 * * * *",
    catchup=False
) as dag:

    quality_check = PythonOperator(
        task_id="quality_check",
        python_callable=run_quality_check
    )

    anomaly_detection = PythonOperator(
        task_id="anomaly_detection",
        python_callable=run_anomaly_detection
    )

    quality_check >> anomaly_detection