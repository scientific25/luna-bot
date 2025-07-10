FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y ca-certificates
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]