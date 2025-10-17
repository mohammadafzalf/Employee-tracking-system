# reports.py
from db_connections import get_sql_connection, get_mongo_connection
import numpy as np

def generate_employee_project_report():
    conn, cur = get_sql_connection()
    cur.execute("""
        SELECT E.first_name || ' ' || E.last_name AS EmployeeName,
               P.project_name AS ProjectName,
               EP.role AS Role,
               EP.assignment_date AS AssignedDate
        FROM EmployeeProjects EP
        JOIN Employees E ON EP.employee_id = E.employee_id
        JOIN Projects P ON EP.project_id = P.project_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def generate_employee_performance_summary(employee_id):
    conn, cur = get_sql_connection()
    cur.execute("SELECT first_name, last_name FROM Employees WHERE employee_id=?", (employee_id,))
    emp = cur.fetchone()
    conn.close()

    collection = get_mongo_connection()
    reviews = list(collection.find({"employee_id": employee_id}, {"_id": 0}))

    if not reviews:
        return f"No reviews found for employee {employee_id}"

    avg_rating = np.mean([r.get("overall_rating", 0) for r in reviews])
    strengths = [r.get("strengths", "") for r in reviews]
    areas = [r.get("areas_for_improvement", "") for r in reviews]

    summary = {
        "Employee": f"{emp[0]} {emp[1]}",
        "Average Rating": round(avg_rating, 2),
        "Strengths": strengths,
        "Areas for Improvement": areas
    }
    return summary
