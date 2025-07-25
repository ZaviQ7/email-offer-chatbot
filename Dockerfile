FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api api
ENV PYTHONUNBUFFERED=1

CMD ["python", "api/api.py"]
