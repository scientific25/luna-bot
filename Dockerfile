FROM python:3.11

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y ca-certificates
RUN pip install --no-cache-dir -r requirements.txt

# Não defina ENV PORT! Deixe o Railway setar.

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} main:app"]
