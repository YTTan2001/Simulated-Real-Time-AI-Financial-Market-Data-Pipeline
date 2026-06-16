from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

from scripts.anomaly_detection import run_anomaly_detection
from scripts.alert import send_email


with DAG(
    dag_id="reporting_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="*/5 * * * *",
    catchup=False
) as dag:

    anomaly_detection = PythonOperator(
        task_id="anomaly_detection",
        python_callable=run_anomaly_detection
    )

    alerting = PythonOperator(
        task_id="send_alert",
        python_callable=send_email
    )

    anomaly_detection >> alerting