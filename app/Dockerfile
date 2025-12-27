FROM python:3.12-slim

WORKDIR /app

COPY app.py .

# instala curl via apt (sistema)
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# instala libs Python
RUN pip install flask psycopg[binary]

HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "app.py"]
