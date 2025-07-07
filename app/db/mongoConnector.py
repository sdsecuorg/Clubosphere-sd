"""
File containing the MongoDb constructor class
"""

from dotenv import load_dotenv
from pymongo import MongoClient


class MongoConnector:
    def __init__(self) -> None:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not specified. Aborting")
        client = MongoClient(mongo_uri)
        db = client["clubosphere"]
        self.users = db["users"]
        self.clubs = db["clubs"]
