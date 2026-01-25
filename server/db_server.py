import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from werkzeug.security import generate_password_hash, check_password_hash
import certifi

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where()
)
db = client[DB_NAME]
users_collection = db["user-credentials"]

def create_data(username: str, password: str) -> bool:
    try:
        # Check if user already exists
        if users_collection.find_one({"username": username}):
            return False

        hashed_password = generate_password_hash(password)

        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })

        return True

    except PyMongoError as e:
        print("Signup Error:", e)
        return False


def view_data(username: str, password: str) -> bool:
    try:
        user = users_collection.find_one({"username": username})

        if not user:
            return False

        return check_password_hash(user["password"], password)

    except PyMongoError as e:
        print("Login Error:", e)
        return False


def update_data(username: str, new_password: str) -> bool:
    try:
        hashed_password = generate_password_hash(new_password)

        result = users_collection.update_one(
            {"username": username},
            {"$set": {"password": hashed_password}}
        )

        return result.modified_count == 1

    except PyMongoError as e:
        print("Update Error:", e)
        return False


def delete_data(username: str) -> bool:
    try:
        result = users_collection.delete_one({"username": username})
        return result.deleted_count == 1

    except PyMongoError as e:
        print("Delete Error:", e)
        return False
