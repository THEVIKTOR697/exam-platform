FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    curl \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker", "--threads", "2","--timeout", "120","-w", "2","--keep-alive", "5","--max-requests", "1000", "--max-requests-jitter", "100","-b", "0.0.0.0:8000","app.main:app"]
