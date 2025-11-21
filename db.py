from pymongo import MongoClient

# MongoDB URI with actual credentials
CONNECTION_STRING = "mongodb+srv://transpolymer:transpolymer365@cluster0.2ojpls3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Function to get the database
def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client["transpolymerDB"]

# Get users collection
db = get_database()
users_collection = db["users"]

# Insert a new user
def insert_user(user_data):
    users_collection.insert_one(user_data)

# Find a user by email
def find_user_by_email(email):
    return users_collection.find_one({"email": email})

# ✅ ADD THIS: Find a user by username
def find_user_by_username(username):
    return users_collection.find_one({"username": username})