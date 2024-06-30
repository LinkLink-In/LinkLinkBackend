FROM python:3.11-slim-buster

WORKDIR /unit-tests

COPY requirements-frozen.txt .
RUN pip install --no-cache-dir --upgrade -r requirements-frozen.txt

COPY ./app ./app
COPY ./tests ./tests

CMD ["python3", "-m", "pytest", "-v", "tests/unit"]
