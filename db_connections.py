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
