"""
File containing classes used to verify data
"""

import re
from bson.objectid import ObjectId


class DataCheck:
    """
    Class used to verify data such as username, passwords ,email ..
    """

    def check_username(self, username: str) -> bool:
        """Check whether the username is valid.

        Args:
            username (str): username to verify

        Returns:
            bool: True if username is valid. Otherwise False.
        """
        pattern = re.compile(r"^[a-zA-Z0-9_]{3,30}$")
        return bool(pattern.match(username))

    def check_email(self, email: str) -> bool:
        """Function used to check the regex of emails

        Args:
            email (str): email string

        Returns:
            bool : True if valid otherwise False.
        """
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
        return bool(pattern.match(email))

    def valid_mongo_id(self, oid: str) -> bool:
        """Function that checks if the oid is valid

        Args:
            oid (str): oid string

        Returns:
            bool: True if valid otherwise False.
        """
        return ObjectId.is_valid(oid)
