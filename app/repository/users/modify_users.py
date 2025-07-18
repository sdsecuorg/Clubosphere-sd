"""
File containing classes that modifies user data
"""

from bson import ObjectId
from datetime import datetime, timedelta, timezone

from app.db.mongo_connector import MongoConnector


class ModifyUsers(MongoConnector):
    """Class that contains functions that update, insert, delete
       data inside the `user` mongo collection.

    Args:
        MongoConnector (_type_): DB connector object
    """

    def __init__(self) -> None:
        super().__init__()

    def add_new_user(self, db_document: dict[str, str]) -> bool:
        """This functions adds a new user to the users col

        Args:
            db_document (dict[str,str]): dict containing the following :
                                    {'username':'','email':'','password':'',role:''}

        Returns:
            bool: True if inserted successfully, otherwise False
        """
        return self.users.insert_one(db_document).inserted_id is not None

    def add_new_token(self, token: str, email: str) -> bool:
        """Function that adds/updates a user's session token

        Args:
            token (str): generated safe token
            email (str): used to identify the user

        Returns:
            bool: True if success. False otherwise
        """
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=300)
        update_doc = {"token": str(token), "expires_at": expires_at}
        results = self.users.update_one({"email": str(email)}, {"$set": update_doc})
        if results.modified_count == 0:
            return False
        return True
