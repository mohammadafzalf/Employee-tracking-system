# app.py
import streamlit as st
from datetime import date
import pandas as pd

# Import all backend functions
from employee_manager import (
    add_employee, get_employee_by_id, list_all_employees
)
from project_manager import (
    add_project, assign_employee_to_project, get_projects_for_employee
)
from performance_reviewer import (
    submit_performance_review, get_performance_reviews_for_employee
)
from reports import (
    generate_employee_project_report, generate_employee_performance_summary
)

# Streamlit Page Config
st.set_page_config(page_title="Employee Performance Tracker", layout="wide")
st.title("🏢 Employee Performance Tracking System")

# Sidebar Menu
menu = st.sidebar.radio(
    "Select Action",
    [
        "Add Employee",
        "Add Project",
        "Assign Employee to Project",
        "Submit Performance Review",
        "View Employee Projects",
        "View Employee Performance",
        "Generate Reports",
        "View All Employees"
    ]
)

# ==========================
# 1️⃣ Add Employee
# ==========================
if menu == "Add Employee":
    st.header("➕ Add New Employee")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    hire_date = st.date_input("Hire Date", value=date.today())
    department = st.text_input("Department")

    if st.button("Add Employee"):
        success, msg = add_employee(first_name, last_name, email, str(hire_date), department)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ==========================
# 2️⃣ Add Project
# ==========================
elif menu == "Add Project":
    st.header("📁 Add New Project")
    project_name = st.text_input("Project Name")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.text_input("End Date (optional)")
    status = st.selectbox("Status", ["Planning", "Ongoing", "Completed"])

    if st.button("Add Project"):
        success, msg = add_project(project_name, str(start_date), end_date, status)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ==========================
# 3️⃣ Assign Employee to Project
# ==========================
elif menu == "Assign Employee to Project":
    st.header("👥 Assign Employee to Project")
    employee_id = st.number_input("Employee ID", min_value=1)
    project_id = st.number_input("Project ID", min_value=1)
    role = st.text_input("Role")

    if st.button("Assign"):
        success, msg = assign_employee_to_project(employee_id, project_id, role)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ==========================
# 4️⃣ Submit Performance Review
# ==========================
elif menu == "Submit Performance Review":
    st.header("📝 Submit Performance Review")
    employee_id = st.number_input("Employee ID", min_value=1)
    reviewer_name = st.text_input("Reviewer Name")
    review_date = st.date_input("Review Date", value=date.today())
    overall_rating = st.slider("Overall Rating", 1, 10, 5)
    strengths = st.text_area("Strengths")
    areas_for_improvement = st.text_area("Areas for Improvement")
    comments = st.text_area("Comments")
    goals_for_next_period = st.text_area("Goals for Next Period")

    if st.button("Submit Review"):
        success, msg = submit_performance_review(
            employee_id, str(review_date), reviewer_name, overall_rating,
            strengths, areas_for_improvement, comments, goals_for_next_period
        )
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ==========================
# 5️⃣ View Employee Projects
# ==========================
elif menu == "View Employee Projects":
    st.header("📋 View Projects for Employee")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    if st.button("Fetch Projects"):
        projects = get_projects_for_employee(employee_id)
        if projects:
            df = pd.DataFrame(projects, columns=["Project Name", "Role", "Assigned Date"])
            st.dataframe(df)
        else:
            st.info("No projects found for this employee.")

# ==========================
# 6️⃣ View Employee Performance
# ==========================
elif menu == "View Employee Performance":
    st.header("📊 View Employee Performance")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    if st.button("Fetch Performance"):
        reviews = get_performance_reviews_for_employee(employee_id)
        if reviews:
            df = pd.DataFrame(reviews)
            st.dataframe(df)
        else:
            st.warning("No performance reviews found for this employee.")

# ==========================
# 7️⃣ Generate Reports
# ==========================
elif menu == "Generate Reports":
    st.header("📈 Generate Reports")
    report_type = st.selectbox("Select Report Type", ["Employee-Project Report", "Performance Summary"])

    if report_type == "Employee-Project Report":
        if st.button("Generate"):
            data = generate_employee_project_report()
            if data:
                df = pd.DataFrame(data, columns=["Employee", "Project", "Role", "Assigned Date"])
                st.dataframe(df)
            else:
                st.info("No report data available.")

    elif report_type == "Performance Summary":
        emp_id = st.number_input("Enter Employee ID for Summary", min_value=1)
        if st.button("Generate Summary"):
            summary = generate_employee_performance_summary(emp_id)
            if isinstance(summary, dict):
                st.subheader(f"Performance Summary for {summary['Employee']}")
                st.write(f"⭐ Average Rating: {summary['Average Rating']}")
                st.write("### Strengths")
                st.write("\n".join(summary['Strengths']))
                st.write("### Areas for Improvement")
                st.write("\n".join(summary['Areas for Improvement']))
            else:
                st.info(summary)

# ==========================
# 8️⃣ View All Employees
# ==========================
elif menu == "View All Employees":
    st.header("👨‍💼 All Employees")
    employees = list_all_employees()
    if employees:
        df = pd.DataFrame(employees, columns=["ID", "First Name", "Last Name", "Email", "Hire Date", "Department"])
        st.dataframe(df)
    else:
        st.warning("No employees found.")
