FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py database.py ./
COPY templates ./templates
COPY static ./static

RUN mkdir -p /data && useradd --create-home appuser \
    && chown -R appuser:appuser /app /data

ENV CAMPUSCARE_DATABASE=/data/campuscare.db
USER appuser

EXPOSE 5000
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "app:app"]
