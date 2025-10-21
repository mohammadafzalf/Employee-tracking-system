from db_connections import get_sql_connection, get_mongo_connection
import numpy as np

def generate_employee_performance_summary(employee_id):
    """
    Generates a detailed performance summary for a given employee,
    including average scores for all metrics and qualitative feedback.
    """
    # --- Fetch Employee Name from SQL ---
    conn, cur = get_sql_connection()
    if not conn:
        return "Database connection failed."

    cur.execute("SELECT first_name, last_name FROM Employees WHERE employee_id=?", (employee_id,))
    emp = cur.fetchone()
    conn.close()

    if not emp:
        return f"No employee found with ID {employee_id}"

    employee_name = f"{emp[0]} {emp[1]}"

    # --- Fetch Reviews from MongoDB ---
    connections = get_mongo_connection()
    if not connections:
        return "MongoDB connection failed."
    
    collection = connections["performance_reviews_db"]["reviews"]

    reviews = list(collection.find({"employee_id": int(employee_id)}, {"_id": 0}))
    if not reviews:
        return f"No reviews found for employee {employee_id}"

    # --- Compute Average Metrics ---
    metrics = ["on_time_delivery", "quality_of_work", "team_collaboration", "problem_solving", "communication"]
    metric_avgs = {}

    for metric in metrics:
        metric_values = [r.get(metric, 0) for r in reviews if isinstance(r.get(metric), (int, float))]
        if metric_values:
            metric_avgs[metric] = round(np.mean(metric_values), 2)
        else:
            metric_avgs[metric] = "N/A"

    overall_ratings = [r.get("overall_rating", 0) for r in reviews if isinstance(r.get("overall_rating"), (int, float))]
    avg_overall_rating = round(np.mean(overall_ratings), 2) if overall_ratings else "N/A"

    # --- Collect Text Feedback ---
    strengths = [r.get("strengths", "") for r in reviews if r.get("strengths")]
    areas = [r.get("areas_for_improvement", "") for r in reviews if r.get("areas_for_improvement")]
    comments = [r.get("comments", "") for r in reviews if r.get("comments")]
    goals = [r.get("goals_for_next_period", "") for r in reviews if r.get("goals_for_next_period")]

    # --- Create Summary Dict ---
    summary = {
        "Employee": employee_name,
        "Average Rating": avg_overall_rating,
        "Average On-Time Delivery": metric_avgs["on_time_delivery"],
        "Average Quality of Work": metric_avgs["quality_of_work"],
        "Average Team Collaboration": metric_avgs["team_collaboration"],
        "Average Problem Solving": metric_avgs["problem_solving"],
        "Average Communication": metric_avgs["communication"],
        "Strengths": strengths,
        "Areas for Improvement": areas,
        "Comments": comments,
        "Goals for Next Period": goals
    }

    return summary


def generate_employee_project_report():
    """
    Generates a report showing each employee and the projects they are assigned to,
    along with their role and assignment date.
    """
    conn, cur = get_sql_connection()
    if not conn:
        return []

    try:
        cur.execute("""
            SELECT 
                E.first_name || ' ' || E.last_name AS EmployeeName,
                P.project_name AS ProjectName,
                EP.role AS Role,
                EP.assignment_date AS AssignedDate
            FROM EmployeeProjects EP
            JOIN Employees E ON EP.employee_id = E.employee_id
            JOIN Projects P ON EP.project_id = P.project_id
            ORDER BY E.first_name, P.project_name
        """)
        rows = cur.fetchall()
        conn.close()

        # Convert to list of dicts for better readability in Streamlit
        formatted_data = [
            {
                "Employee": row[0],
                "Project": row[1],
                "Role": row[2],
                "Assigned Date": row[3]
            }
            for row in rows
        ]

        return formatted_data

    except Exception as e:
        print("❌ Error generating project report:", e)
        return []
