"""
File containing classes that retrieves and finds users
"""

from app.db.mongo_connector import MongoConnector
from bson import ObjectId


class RetrieveUsers(MongoConnector):
    def __init__(self) -> None:
        """
        Constructor
        """
        super().__init__()

    def find_user_using_oid(self, oid: str) -> dict[str, str] | None:
        """
            Function that finds a user using their oid
        Args:
            oid (str): valid oid

        Returns:
            dict[str,str]: user document
        """
        return self.users.find_one({"_id": ObjectId(str(oid))})

    def find_user_using_username(self, username: str) -> dict[str, str] | None:
        """Function that finds a user by his username

        Args:
            username (str): username of the user

        Returns:
            dict[str,str] | None: returns a dict if a document has been found, otherwise None
        """
        return self.users.find_one({"username": str(username)})

    def find_user_using_email(self, email: str) -> dict[str, str] | None:
        """Function that finds a user by his email

        Args:
            username (str): email of the user

        Returns:
            dict[str,str] | None: returns a dict if a document has been found, otherwise None
        """
        return self.users.find_one({"email": str(email)})
