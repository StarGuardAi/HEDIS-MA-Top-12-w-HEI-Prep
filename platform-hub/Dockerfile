# Platform Hub — Shiny on HuggingFace Spaces
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
