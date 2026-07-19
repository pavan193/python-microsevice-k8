import os
import time

from flask import Flask, jsonify, request
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "employee_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_db_connection():

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row
    )


def init_db():

    retries = 10

    while retries > 0:

        try:

            with get_db_connection() as conn:

                with conn.cursor() as cursor:

                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS employees (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            email VARCHAR(150) NOT NULL UNIQUE,
                            role VARCHAR(100) NOT NULL
                        )
                        """
                    )

                conn.commit()

            print("Employee database initialized successfully.")

            return

        except Exception as error:

            retries -= 1

            print(
                f"Employee database connection failed: {error}"
            )

            print(
                f"Retries remaining: {retries}"
            )

            time.sleep(5)

    raise Exception(
        "Employee Service could not connect to database."
    )


@app.route("/employees", methods=["GET"])
def get_employees():

    with get_db_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, name, email, role
                FROM employees
                ORDER BY id DESC
                """
            )

            employees = cursor.fetchall()

    return jsonify(employees)


@app.route("/employees", methods=["POST"])
def create_employee():

    data = request.get_json()

    if not data:

        return jsonify(
            error="JSON body is required."
        ), 400

    name = data.get("name")
    email = data.get("email")
    role = data.get("role")

    if not name or not email or not role:

        return jsonify(
            error="name, email and role are required."
        ), 400

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO employees
                    (name, email, role)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, email, role
                    """,
                    (
                        name,
                        email,
                        role
                    )
                )

                employee = cursor.fetchone()

            conn.commit()

        return jsonify(employee), 201

    except psycopg.errors.UniqueViolation:

        return jsonify(
            error="Employee email already exists."
        ), 409


@app.route(
    "/employees/<int:employee_id>",
    methods=["DELETE"]
)
def delete_employee(employee_id):

    with get_db_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM employees
                WHERE id = %s
                RETURNING id
                """,
                (employee_id,)
            )

            deleted_employee = cursor.fetchone()

        conn.commit()

    if deleted_employee is None:

        return jsonify(
            error="Employee not found."
        ), 404

    return jsonify(
        message="Employee deleted successfully."
    )


@app.route("/health", methods=["GET"])
def health():

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute("SELECT 1")

        return jsonify(
            service="employee-service",
            status="UP",
            database="CONNECTED"
        ), 200

    except Exception as error:

        return jsonify(
            service="employee-service",
            status="DOWN",
            database="DISCONNECTED",
            error=str(error)
        ), 503


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5001
    )