# Multi-stage build for better caching and smaller final image
FROM python:3.10-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

FROM base as development

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for-db.sh

EXPOSE 5000

CMD ["./wait-for-db.sh", "flask", "run", "--host=0.0.0.0", "--debug"]

FROM base as production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

RUN chmod +x wait-for-db.sh

EXPOSE 5000

CMD ["./wait-for-db.sh", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"] 