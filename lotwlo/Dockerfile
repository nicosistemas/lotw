FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY lotwlo ./lotwlo
COPY web ./web

ENV PYTHONPATH=/app

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5010", "web.app:app"]