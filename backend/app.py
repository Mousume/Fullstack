import os

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "database"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        dbname=os.getenv("DB_NAME", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
    )


def create_tables():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )


@app.get("/")
def home():
    return "Hello, World!"


@app.get("/db")
def database_check():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT NOW()")
            current_time = cursor.fetchone()[0]
    return jsonify({"time": current_time})


@app.get("/users")
def get_users():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email, created_at FROM users ORDER BY id"
            )
            users = cursor.fetchall()

    return jsonify(
        [
            {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "created_at": user[3],
            }
            for user in users
        ]
    )


@app.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                RETURNING id, name, email, created_at
                """,
                (name, email),
            )
            user = cursor.fetchone()

    return jsonify(
        {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "created_at": user[3],
        }
    ), 201


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))