import os

import requests
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


EMPLOYEE_SERVICE_URL = os.getenv(
    "EMPLOYEE_SERVICE_URL",
    "http://localhost:5001"
)

PROJECT_SERVICE_URL = os.getenv(
    "PROJECT_SERVICE_URL",
    "http://localhost:5002"
)


@app.route("/")
def index():

    employees = []
    projects = []

    employee_service_status = "DOWN"
    project_service_status = "DOWN"

    try:

        response = requests.get(
            f"{EMPLOYEE_SERVICE_URL}/employees",
            timeout=5
        )

        if response.ok:

            employees = response.json()

            employee_service_status = "UP"

    except requests.RequestException:

        pass


    try:

        response = requests.get(
            f"{PROJECT_SERVICE_URL}/projects",
            timeout=5
        )

        if response.ok:

            projects = response.json()

            project_service_status = "UP"

    except requests.RequestException:

        pass


    return render_template(
        "index.html",
        employees=employees,
        projects=projects,
        employee_service_status=employee_service_status,
        project_service_status=project_service_status
    )


@app.route("/employees/add", methods=["POST"])
def add_employee():

    employee = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "role": request.form.get("role")
    }

    try:

        requests.post(
            f"{EMPLOYEE_SERVICE_URL}/employees",
            json=employee,
            timeout=5
        )

    except requests.RequestException:

        pass

    return redirect(
        url_for("index")
    )


@app.route(
    "/employees/delete/<int:employee_id>",
    methods=["POST"]
)
def delete_employee(employee_id):

    try:

        requests.delete(
            f"{EMPLOYEE_SERVICE_URL}/employees/{employee_id}",
            timeout=5
        )

    except requests.RequestException:

        pass

    return redirect(
        url_for("index")
    )


@app.route("/projects/add", methods=["POST"])
def add_project():

    project = {
        "name": request.form.get("name"),
        "description": request.form.get("description"),
        "status": request.form.get("status")
    }

    try:

        requests.post(
            f"{PROJECT_SERVICE_URL}/projects",
            json=project,
            timeout=5
        )

    except requests.RequestException:

        pass

    return redirect(
        url_for("index")
    )


@app.route(
    "/projects/delete/<int:project_id>",
    methods=["POST"]
)
def delete_project(project_id):

    try:

        requests.delete(
            f"{PROJECT_SERVICE_URL}/projects/{project_id}",
            timeout=5
        )

    except requests.RequestException:

        pass

    return redirect(
        url_for("index")
    )


@app.route("/health")
def health():

    return {
        "service": "frontend",
        "status": "UP"
    }, 200


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )