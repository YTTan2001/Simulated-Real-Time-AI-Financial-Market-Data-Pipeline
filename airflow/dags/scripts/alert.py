import os
import smtplib

from email.mime.text import MIMEText


def send_email(**context):

    anomaly_count = context["ti"].xcom_pull(
        task_ids="anomaly_detection"
    )

    if anomaly_count == 0:
        print("No anomaly detected")
        return

    message = f"""
    ALERT

    {anomaly_count} anomalies detected.

    Please check Metabase dashboard.
    """

    msg = MIMEText(message)

    msg["Subject"] = "Market Anomaly Alert"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = os.getenv("EMAIL_ADDRESS")

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if email is None or password is None:
        raise Exception(
           "EMAIL_ADDRESS or EMAIL_PASSWORD not found."
        )

    server.login(
        email,
        password
    )


    server.send_message(msg)

    server.quit()

    print("Alert email sent")