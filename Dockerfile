FROM python:3.10-slim

WORKDIR /app
COPY . /app

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

