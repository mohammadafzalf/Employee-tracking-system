# project_manager.py
from db_connections import get_sql_connection

def add_project(project_name, start_date, end_date, status):
    conn, cur = get_sql_connection()
    try:
        cur.execute("""
            INSERT INTO Projects (project_name, start_date, end_date, status)
            VALUES (?, ?, ?, ?)
        """, (project_name, start_date, end_date, status))
        conn.commit()
        return True, "Project added successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()


def assign_employee_to_project(employee_id, project_id, role):
    conn, cur = get_sql_connection()
    try:
        cur.execute("""
            INSERT INTO EmployeeProjects (employee_id, project_id, role)
            VALUES (?, ?, ?)
        """, (employee_id, project_id, role))
        conn.commit()
        return True, "Employee assigned successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()


def get_projects_for_employee(employee_id):
    conn, cur = get_sql_connection()
    cur.execute("""
        SELECT P.project_name, EP.role, EP.assignment_date
        FROM EmployeeProjects EP
        JOIN Projects P ON EP.project_id = P.project_id
        WHERE EP.employee_id = ?
    """, (employee_id,))
    rows = cur.fetchall()
    conn.close()
    return rows
