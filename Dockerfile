FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY wsgi.py .
COPY wait-for-db.sh .

RUN chmod +x wait-for-db.sh

EXPOSE 5000

ENV FLASK_APP=wsgi.py
ENV PYTHONPATH=/app

CMD ["./wait-for-db.sh", "flask", "run", "--host=0.0.0.0"] 