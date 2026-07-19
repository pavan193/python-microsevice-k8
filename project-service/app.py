import os
import time

from flask import Flask, jsonify, request
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "project_db")
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
                        CREATE TABLE IF NOT EXISTS projects (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(150) NOT NULL,
                            description VARCHAR(500),
                            status VARCHAR(50) NOT NULL
                        )
                        """
                    )

                conn.commit()

            print(
                "Project database initialized successfully."
            )

            return

        except Exception as error:

            retries -= 1

            print(
                f"Project database connection failed: {error}"
            )

            print(
                f"Retries remaining: {retries}"
            )

            time.sleep(5)

    raise Exception(
        "Project Service could not connect to database."
    )


@app.route("/projects", methods=["GET"])
def get_projects():

    with get_db_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, name, description, status
                FROM projects
                ORDER BY id DESC
                """
            )

            projects = cursor.fetchall()

    return jsonify(projects)


@app.route("/projects", methods=["POST"])
def create_project():

    data = request.get_json()

    if not data:

        return jsonify(
            error="JSON body is required."
        ), 400

    name = data.get("name")

    description = data.get(
        "description",
        ""
    )

    status = data.get(
        "status",
        "Planning"
    )

    if not name:

        return jsonify(
            error="Project name is required."
        ), 400

    with get_db_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO projects
                (name, description, status)
                VALUES (%s, %s, %s)
                RETURNING id, name, description, status
                """,
                (
                    name,
                    description,
                    status
                )
            )

            project = cursor.fetchone()

        conn.commit()

    return jsonify(project), 201


@app.route(
    "/projects/<int:project_id>",
    methods=["DELETE"]
)
def delete_project(project_id):

    with get_db_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM projects
                WHERE id = %s
                RETURNING id
                """,
                (project_id,)
            )

            deleted_project = cursor.fetchone()

        conn.commit()

    if deleted_project is None:

        return jsonify(
            error="Project not found."
        ), 404

    return jsonify(
        message="Project deleted successfully."
    )


@app.route("/health", methods=["GET"])
def health():

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute("SELECT 1")

        return jsonify(
            service="project-service",
            status="UP",
            database="CONNECTED"
        ), 200

    except Exception as error:

        return jsonify(
            service="project-service",
            status="DOWN",
            database="DISCONNECTED",
            error=str(error)
        ), 503


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5002
    )