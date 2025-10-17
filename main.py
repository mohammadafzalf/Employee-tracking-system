# app.py
import streamlit as st
from datetime import date

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
        "Generate Reports"
    ]
)

# --- Add Employee ---
if menu == "Add Employee":
    st.header("➕ Add New Employee")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    hire_date = st.date_input("Hire Date", value=date.today())
    department = st.text_input("Department")

    if st.button("Add Employee"):
        # Placeholder for database function
        # add_employee(first_name, last_name, email, hire_date, department)
        st.success(f"Employee '{first_name} {last_name}' added successfully!")

# --- Add Project ---
elif menu == "Add Project":
    st.header("📁 Add New Project")
    project_name = st.text_input("Project Name")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date (optional)", value=None)
    status = st.selectbox("Status", ["Planning", "Ongoing", "Completed"])

    if st.button("Add Project"):
        # add_project(project_name, start_date, end_date, status)
        st.success(f"Project '{project_name}' added successfully!")

# --- Assign Employee to Project ---
elif menu == "Assign Employee to Project":
    st.header("👥 Assign Employee to Project")
    employee_id = st.number_input("Employee ID", min_value=1)
    project_id = st.number_input("Project ID", min_value=1)
    role = st.text_input("Role")

    if st.button("Assign"):
        # assign_employee_to_project(employee_id, project_id, role)
        st.success(f"Employee {employee_id} assigned to Project {project_id} as {role}")

# --- Submit Performance Review ---
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
        # submit_performance_review(employee_id, review_date, reviewer_name, overall_rating, strengths, areas_for_improvement, comments, goals_for_next_period)
        st.success(f"Review submitted successfully for Employee {employee_id}")

# --- View Employee Projects ---
elif menu == "View Employee Projects":
    st.header("📋 View Projects for Employee")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    if st.button("Fetch Projects"):
        # projects = get_projects_for_employee(employee_id)
        # st.table(projects)
        st.info("Projects displayed here (coming soon)")

# --- View Employee Performance ---
elif menu == "View Employee Performance":
    st.header("📊 View Employee Performance")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    if st.button("Fetch Performance"):
        # reviews = get_performance_reviews_for_employee(employee_id)
        # st.table(reviews)
        st.info("Performance data displayed here (coming soon)")

# --- Generate Reports ---
elif menu == "Generate Reports":
    st.header("📈 Generate Reports")
    report_type = st.selectbox("Select Report Type", ["Employee-Project Report", "Performance Summary"])

    if report_type == "Employee-Project Report":
        if st.button("Generate"):
            # generate_employee_project_report()
            st.info("Employee-Project report generated (coming soon)")

    elif report_type == "Performance Summary":
        emp_id = st.number_input("Enter Employee ID for Summary", min_value=1)
        if st.button("Generate Summary"):
            # generate_employee_performance_summary(emp_id)
            st.info("Performance Summary displayed here (coming soon)")
