# employee_manager.py
from db_connections import get_sql_connection

def add_employee(first_name, last_name, email, hire_date, department):
    conn, cur = get_sql_connection()
    try:
        cur.execute("""
            INSERT INTO Employees (first_name, last_name, email, hire_date, department)
            VALUES (?, ?, ?, ?, ?)
        """, (first_name, last_name, email, hire_date, department))
        conn.commit()
        return True, "Employee added successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()


def get_employee_by_id(employee_id):
    conn, cur = get_sql_connection()
    cur.execute("SELECT * FROM Employees WHERE employee_id=?", (employee_id,))
    employee = cur.fetchone()
    conn.close()
    return employee


def list_all_employees():
    conn, cur = get_sql_connection()
    cur.execute("SELECT * FROM Employees")
    rows = cur.fetchall()
    conn.close()
    return rows