FROM python:3.11-slim

WORKDIR /

RUN usr/local/bin/python -m pip install --upgrade pip
COPY ./app /app/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
CMD ["python3", "-m", "app"]
