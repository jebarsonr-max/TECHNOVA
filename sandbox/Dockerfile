FROM python:3.11-slim

WORKDIR /app

# Disable network access during build and runtime
RUN pip install --no-cache-dir pandas duckdb numpy openpyxl pyarrow

COPY runner.py /app/runner.py

# Run as non-root user for security
RUN useradd -m sandboxuser
USER sandboxuser

ENTRYPOINT ["python", "/app/runner.py"]
