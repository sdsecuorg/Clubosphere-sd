"""
File containing classes that retrieves and finds users
"""

from app.db.mongoConnector import MongoConnector
from bson import ObjectId


class RetrieveUsers(MongoConnector()):
    def __init__(self) -> None:
        """
        Constructor
        """
        super().__init__(self)

    def find_user_using_oid(self, oid: str) -> dict[str, str] | None:
        """
            Function that finds a user using their oid
        Args:
            oid (str): valid oid

        Returns:
            dict[str,str]: user document
        """
        return self.users.find_one({"_id": ObjectId(str(oid))})
