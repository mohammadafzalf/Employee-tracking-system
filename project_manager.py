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

def list_all_projects():
    """Lists all projects with their ID for viewing and status update."""
    conn, cur = get_sql_connection()
    cur.execute("""
        SELECT project_id, project_name, start_date, end_date, status
        FROM Projects
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def update_project_status(project_id, new_status):
    """Updates the status of a specific project by ID."""
    conn, cur = get_sql_connection()
    try:
        cur.execute("""
            UPDATE Projects
            SET status = ?
            WHERE project_id = ?
        """, (new_status, project_id))
        conn.commit()
        if cur.rowcount > 0:
            return True, f"Project ID {project_id} status updated to {new_status}."
        else:
            return False, f"Project ID {project_id} not found."
    except Exception as e:
        return False, f"Error updating project status: {str(e)}"
    finally:
        conn.close()
