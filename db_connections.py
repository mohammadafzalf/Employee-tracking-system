# db_connections.py
import sqlite3
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_connection_string = os.getenv("connection_string")

# ---------- SQL (SQLite) ----------
def get_sql_connection():
    try:
        conn = sqlite3.connect("company.db")
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("Failed to connect to SQLite: ", e)
    


# ---------- NoSQL (MongoDB) ----------
def get_mongo_connection():
    try:
        print(mongo_connection_string)
        mongo_client = MongoClient("mongo_connection_string")
        db = mongo_client["performance_reviews_db"]
        collection = db["reviews"]
        return mongo_client,collection
    except Exception as e:
        print("Failed to connect to MongoDB: ", e)
        
        
# Relational Database Schema (SQLite)
""" Table: employees """
 # Create Employees table
def create_table_employees(conn, cur):
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hire_date TEXT,
            department TEXT
        )
        """)
        conn.commit()
    except Exception as e:
        print("Error creating Employees table: ", e)

""" Table: projects """
def create_table_projects(conn, cur):
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            status TEXT
        )
        """)
        conn.commit()
    except Exception as e:
        print("Error creating Projects table: ", e)
    
""" Table: EmployeeProjects """    
def create_table_employee_projects(conn, cur):
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS EmployeeProjects (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            project_id INTEGER,
            role TEXT,
            assignment_date TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
            FOREIGN KEY (project_id) REFERENCES Projects(project_id)
        )
        """)
        conn.commit()
    except Exception as e:
        print("Error creating EmployeeProjects table: ", e)
           
def initialize_database():
    conn, cur = get_sql_connection()
    create_table_employees(conn, cur)
    create_table_projects(conn, cur)
    create_table_employee_projects(conn, cur)
    

initialize_database()