FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements-frozen.txt .
RUN pip install --no-cache-dir --upgrade -r requirements-frozen.txt

COPY /app .

CMD sleep 10 && alembic upgrade head && \
 python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload \
  --proxy-headers --forwarded-allow-ips '*'
