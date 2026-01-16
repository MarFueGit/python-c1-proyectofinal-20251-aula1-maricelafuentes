FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data && chmod 777 /app/data

COPY . .

EXPOSE 5000

ENTRYPOINT ["sh", "entrypoint.sh"]