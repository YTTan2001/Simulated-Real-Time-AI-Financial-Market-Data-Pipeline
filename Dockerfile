FROM apache/airflow:2.9.1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default command (overridden by docker-compose)
CMD ["bash"]