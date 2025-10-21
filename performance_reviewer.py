from db_connections import get_mongo_connection

def submit_performance_review(
    employee_id, review_date, reviewer_name, overall_rating,
    strengths, areas_for_improvement, comments, goals_for_next_period,
    on_time_delivery, quality_of_work, team_collaboration,
    problem_solving, communication
):
    try:
        connection = get_mongo_connection()
        collection = connection["performance_reviews_db"]["reviews"]

        review_doc = {
            "employee_id": int(employee_id),
            "review_date": review_date,
            "reviewer_name": reviewer_name,
            "on_time_delivery": on_time_delivery,
            "quality_of_work": quality_of_work,
            "team_collaboration": team_collaboration,
            "problem_solving": problem_solving,
            "communication": communication,
            "overall_rating": round(overall_rating, 2),
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "comments": comments,
            "goals_for_next_period": goals_for_next_period
        }

        collection.insert_one(review_doc)
        return True, f"✅ Review submitted successfully for Employee ID {employee_id}"

    except Exception as e:
        return False, f"❌ Failed to submit review: {str(e)}"



def get_performance_reviews_for_employee(employee_id):
    """
    Fetch all performance reviews for a given employee from MongoDB.
    Includes structured metric scores and qualitative feedback.
    """
    try:
        connections = get_mongo_connection()
        if not connections:
            print("❌ MongoDB connection failed.")
            return []
        collection = connections["performance_reviews_db"]["reviews"]
        reviews = list(collection.find({"employee_id": int(employee_id)}, {"_id": 0}))

        if not reviews:
            return []

        formatted_reviews = []
        for r in reviews:
            formatted_reviews.append({
                "Review Date": r.get("review_date", "N/A"),
                "Reviewer Name": r.get("reviewer_name", "N/A"),
                "On-Time Delivery": r.get("on_time_delivery", "N/A"),
                "Quality of Work": r.get("quality_of_work", "N/A"),
                "Team Collaboration": r.get("team_collaboration", "N/A"),
                "Problem Solving": r.get("problem_solving", "N/A"),
                "Communication": r.get("communication", "N/A"),
                "Overall Rating": r.get("overall_rating", "N/A"),
                "Strengths": r.get("strengths", "N/A"),
                "Areas for Improvement": r.get("areas_for_improvement", "N/A"),
                "Comments": r.get("comments", "N/A"),
                "Goals for Next Period": r.get("goals_for_next_period", "N/A")
            })

        return formatted_reviews

    except Exception as e:
        print("❌ Error fetching performance reviews:", e)
        return []
