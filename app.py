import os
import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

def get_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        connect_timeout=3
    )

@app.route("/")
def hello():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS acessos (
                    id SERIAL PRIMARY KEY,
                    total INT NOT NULL
                )
            """)
            cur.execute("SELECT total FROM acessos LIMIT 1")
            row = cur.fetchone()

            total = 1 if row is None else row[0] + 1
            cur.execute("DELETE FROM acessos")
            cur.execute("INSERT INTO acessos (total) VALUES (%s)", (total,))

    return jsonify(acessos=total)

@app.route("/health")
def health():
    try:
        with get_conn():
            return jsonify(status="ok"), 200
    except Exception:
        return jsonify(status="error"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", 8080)))
