# performance_reviewer.py
from db_connections import get_mongo_connection

def submit_performance_review(employee_id, review_date, reviewer_name,
                              overall_rating, strengths, areas_for_improvement,
                              comments, goals_for_next_period):
    mongo_client = get_mongo_connection()
    db = mongo_client["performance_reviews_db"]
    collection = db["reviews"]
    review_doc = {
        "employee_id": employee_id,
        "review_date": str(review_date),
        "reviewer_name": reviewer_name,
        "overall_rating": overall_rating,
        "strengths": strengths,
        "areas_for_improvement": areas_for_improvement,
        "comments": comments,
        "goals_for_next_period": goals_for_next_period
    }
    try:
        collection.insert_one(review_doc)
        return True, "Review submitted successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_performance_reviews_for_employee(employee_id):
    mongo_client = get_mongo_connection()
    db = mongo_client["performance_reviews_db"]
    collection = db["reviews"]
    reviews = list(collection.find({"employee_id": employee_id}, {"_id": 0}))
    return reviews
