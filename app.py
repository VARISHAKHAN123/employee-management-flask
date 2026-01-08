from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
FILE = "employees.json"


def load_employees():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_employees(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    employees = load_employees()
    return render_template("add_employee.html", employees=employees)


@app.route("/submit", methods=["POST"])
def submit():
    employees = load_employees()

    emp = {
        "id": len(employees) + 1,
        "name": request.form["name"],
        "department": request.form["department"],
        "salary": request.form["salary"]
    }

    employees.append(emp)
    save_employees(employees)

    return redirect("/")

@app.route("/delete/<int:emp_id>")
def delete_employee(emp_id):
    employees = load_employees()

    employees = [emp for emp in employees if emp["id"] != emp_id]

    save_employees(employees)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
