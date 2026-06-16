FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir kafka-python-ng pandas

# Copy the producer script into the container
COPY kafka/producer.py ./kafka/

# Run the script when the container starts
CMD ["python", "-u", "kafka/producer.py"]