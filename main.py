import streamlit as st
from datetime import date
import pandas as pd

# Import all backend functions (Note: These modules must exist in your environment)
# For this code to run successfully, you need:
# - employee_manager.py
# - project_manager.py
# - performance_reviewer.py
# - reports.py

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

# ==========================
# 🔐 Step 1: Role-based Login System
# ==========================

USER_CREDENTIALS = {
    "hr_user": {"password": "hr@123", "role": "HR"},
    "teamlead_user": {"password": "lead@123", "role": "Team Lead"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.sidebar.header("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = USER_CREDENTIALS.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = user["role"]
            st.rerun() # Rerun to switch from login to dashboard
        else:
            st.sidebar.error("❌ Invalid credentials.")
            
    # CRITICAL: Stop execution here if the user is not logged in
    st.stop()


# ==========================
# 🚪 Step 2: Logout Button
# ==========================

st.sidebar.write("---")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# ==========================
# 🧭 Step 3: Role-based Menu
# ==========================

if st.session_state.role == "HR":
    menu = st.sidebar.radio(
        "Select Action",
        [
            "Add Employee",
            "View All Employees",
            "View Employee Performance",
            "Generate Reports"
        ]
    )
elif st.session_state.role == "Team Lead":
    menu = st.sidebar.radio(
        "Select Action",
        [
            "Add Project",
            "Assign Employee to Project",
            "Submit Performance Review",
            "View Employee Projects",
            "View Employee Performance",
            "Generate Reports"
        ]
    )
else:
    st.warning("You do not have access to this system.")
    st.stop()

# ==========================
# 1️⃣ Add Employee (HR Only)
# ==========================

if menu == "Add Employee" and st.session_state.role == "HR":
    st.header("➕ Add New Employee")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    hire_date = st.date_input("Hire Date", value=date.today())
    department = st.text_input("Department")

    if st.button("Add Employee"):
        success, msg = add_employee(first_name, last_name, email, str(hire_date), department)
        st.success(msg) if success else st.error(msg)


# ==========================
# 2️⃣ Add Project (Team Lead)
# ==========================

elif menu == "Add Project" and st.session_state.role == "Team Lead":
    st.header("📁 Add New Project")
    project_name = st.text_input("Project Name")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.text_input("End Date (optional)")
    status = st.selectbox("Status", ["Planning", "Ongoing", "Completed"])

    if st.button("Add Project"):
        success, msg = add_project(project_name, str(start_date), end_date, status)
        st.success(msg) if success else st.error(msg)


# ==========================
# 3️⃣ Assign Employee to Project (Team Lead)
# ==========================

elif menu == "Assign Employee to Project" and st.session_state.role == "Team Lead":
    st.header("👥 Assign Employee to Project")
    employee_id = st.number_input("Employee ID", min_value=1)
    project_id = st.number_input("Project ID", min_value=1)
    role = st.text_input("Role")

    if st.button("Assign"):
        success, msg = assign_employee_to_project(employee_id, project_id, role)
        st.success(msg) if success else st.error(msg)

# ==========================
# 4️⃣ Submit Performance Review (Team Lead)
# ==========================

elif menu == "Submit Performance Review" and st.session_state.role == "Team Lead":
    st.header("📝 Submit Performance Review")

    employee_id = st.number_input("Employee ID", min_value=1)
    reviewer_name = st.text_input("Reviewer Name")
    review_date = st.date_input("Review Date", value=date.today())

    st.subheader("📊 Performance Metrics")

    # Define dropdown options
    metric_options = ["Excellent", "Good", "Average", "Poor"]

    # Create dropdowns for each metric
    on_time_delivery = st.selectbox("On-Time Delivery", metric_options, index=1)
    quality_of_work = st.selectbox("Quality of Work", metric_options, index=1)
    team_collaboration = st.selectbox("Team Collaboration", metric_options, index=1)
    problem_solving = st.selectbox("Problem Solving", metric_options, index=1)
    communication = st.selectbox("Communication Skills", metric_options, index=1)

    # Optional text feedback fields
    st.subheader("🗒️ Additional Feedback")
    strengths = st.text_area("Strengths")
    areas_for_improvement = st.text_area("Areas for Improvement")
    comments = st.text_area("Comments")
    goals_for_next_period = st.text_area("Goals for Next Period")

    if st.button("Submit Review"):
        # Convert dropdown values to numeric scores
        rating_map = {"Excellent": 4, "Good": 3, "Average": 2, "Poor": 1}

        scores = [
            rating_map[on_time_delivery],
            rating_map[quality_of_work],
            rating_map[team_collaboration],
            rating_map[problem_solving],
            rating_map[communication]
        ]
        overall_rating = sum(scores) / len(scores)

        success, msg = submit_performance_review(
            employee_id, str(review_date), reviewer_name, overall_rating,
            strengths, areas_for_improvement, comments, goals_for_next_period,
            rating_map[on_time_delivery],
            rating_map[quality_of_work],
            rating_map[team_collaboration],
            rating_map[problem_solving],
            rating_map[communication]
        )

        st.success(msg) if success else st.error(msg)

# ==========================
# 5️⃣ View Employee Projects (Team Lead)
# ==========================

elif menu == "View Employee Projects" and st.session_state.role == "Team Lead":
    st.header("📋 View Projects for Employee")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    if st.button("Fetch Projects"):
        # Assuming get_projects_for_employee returns a list of dictionaries/tuples
        projects = get_projects_for_employee(employee_id)
        if projects:
            df = pd.DataFrame(projects, columns=["Project Name", "Role", "Assigned Date"])
            st.dataframe(df)
        else:
            st.info("No projects found for this employee.")

# ==========================
# 6️⃣ View Employee Performance (HR + Team Lead)
# ==========================

elif menu == "View Employee Performance":
    st.header("📊 View Employee Performance")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    if st.button("Fetch Performance"):
        # Assuming get_performance_reviews_for_employee returns a list of dictionaries/tuples
        reviews = get_performance_reviews_for_employee(employee_id)
        if reviews:
            # Placeholder: Assuming the function returns structured data
            st.dataframe(pd.DataFrame(reviews))
        else:
            st.warning("No performance reviews found for this employee.")


# ==========================
# 7️⃣ Generate Reports (Both)
# ==========================

elif menu == "Generate Reports":
    st.header("📈 Generate Reports")
    report_type = st.selectbox("Select Report Type", ["Employee-Project Report", "Performance Summary"])

    if report_type == "Employee-Project Report":
        if st.button("Generate Employee-Project Report"):
            data = generate_employee_project_report()
            if data:
                # Placeholder for columns
                st.dataframe(pd.DataFrame(data, columns=["Employee", "Project", "Role", "Assigned Date"]))
            else:
                st.info("No report data available.")

    elif report_type == "Performance Summary":
        emp_id = st.number_input("Enter Employee ID for Summary", min_value=1)
        
        if st.button("Generate Summary"):
            summary = generate_employee_performance_summary(emp_id)

            if isinstance(summary, dict):
                st.subheader(f"📊 Performance Summary for {summary.get('Employee', f'Employee ID {emp_id}')}")
                
                # --- Display Numeric Averages in a Table ---
                metrics_data = {
                    "Metric": [
                        "Overall Rating",
                        "On-Time Delivery",
                        "Quality of Work",
                        "Team Collaboration",
                        "Problem Solving",
                        "Communication"
                    ],
                    "Average Score": [
                        summary.get("Average Rating", "N/A"),
                        summary.get("Average On-Time Delivery", "N/A"),
                        summary.get("Average Quality of Work", "N/A"),
                        summary.get("Average Team Collaboration", "N/A"),
                        summary.get("Average Problem Solving", "N/A"),
                        summary.get("Average Communication", "N/A")
                    ]
                }

                st.table(pd.DataFrame(metrics_data))

                # --- Text Feedback Sections ---
                st.write("### 💪 Strengths")
                if summary.get("Strengths"):
                    for s in summary["Strengths"]:
                        st.markdown(f"- {s}")
                else:
                    st.info("No strengths listed.")

                st.write("### ⚙️ Areas for Improvement")
                if summary.get("Areas for Improvement"):
                    for a in summary["Areas for Improvement"]:
                        st.markdown(f"- {a}")
                else:
                    st.info("No areas for improvement listed.")

                st.write("### 💬 Comments")
                if summary.get("Comments"):
                    for c in summary["Comments"]:
                        st.markdown(f"- {c}")
                else:
                    st.info("No comments available.")

                st.write("### 🎯 Goals for Next Period")
                if summary.get("Goals for Next Period"):
                    for g in summary["Goals for Next Period"]:
                        st.markdown(f"- {g}")
                else:
                    st.info("No goals specified for next period.")

            else:
                st.warning(summary)


# ==========================
# 8️⃣ View All Employees (HR Only)
# ==========================

elif menu == "View All Employees" and st.session_state.role == "HR":
    st.header("👨‍💼 All Employees")
    employees = list_all_employees()
    if employees:
        # Placeholder for columns
        st.dataframe(pd.DataFrame(employees, columns=["ID", "First Name", "Last Name", "Email", "Hire Date", "Department"]))
    else:
        st.warning("No employees found.")
