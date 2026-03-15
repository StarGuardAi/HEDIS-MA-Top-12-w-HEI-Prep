FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies + curl for OPA, then OPA binary (static, no glibc dependency)
RUN apt-get update && apt-get install -y --no-install-recommends curl gcc \
    && rm -rf /var/lib/apt/lists/* \
    && curl -L -o /usr/local/bin/opa \
        https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static \
    && chmod +x /usr/local/bin/opa

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["shiny", "run", "run:app", "--host", "0.0.0.0", "--port", "8000"]
