FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV DATABASE_PATH=/data/app.db

EXPOSE 5000

# Create directory for SQLite DB (to match K8s volume mount)
RUN mkdir -p /data

CMD ["flask", "run", "--port=5000"]
