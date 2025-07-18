"""
File containing classes that modifies user data
"""

from app.db.mongo_connector import MongoConnector
from bson import ObjectId


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
        return self.users.insert_one(db_document).inserted_id == True
