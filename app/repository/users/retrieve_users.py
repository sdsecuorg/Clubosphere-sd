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

    def find_user_using_email(self, email: str) -> dict[str, str] | None:
        """Function that finds a user by his email

        Args:
            username (str): email of the user

        Returns:
            dict[str,str] | None: returns a dict if a document has been found, otherwise None
        """
        return self.users.find_one({"email": str(email)})

    def find_user_using_token(
        self, token: str, safe: bool = True
    ) -> dict[str, str] | None:
        """Function used to find a user using a token session

        Args:
            token (str): session token
            safe (bool): Return only the username,email,expires_at and role number. True by default.
        Returns:
            dict[str,str] | None: user's document
        """
        found_user = self.users.find_one({"token": str(token)})
        if not found_user:
            return None
        if safe:
            doc = {
                "username": found_user["username"],
                "email": found_user["email"],
                "role": found_user["role"],
                "expires_at": found_user["expires_at"],
            }
            return doc
        return found_user
