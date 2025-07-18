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

    def check_password(self, password: str) -> bool:
        """Check the validity of a password.
        The password much be longer than 6 chars,
        include lower/upper case letters, numbers and special chars.

        Args:
            password (str): password string

        Returns:
            bool: True if password meets requirements else False
        """
        ### TO DO
        return True

    def valid_mongo_id(self, oid: str) -> bool:
        """Function that checks if the oid is valid

        Args:
            oid (str): oid string

        Returns:
            bool: True if valid otherwise False.
        """
        return ObjectId.is_valid(oid)

    def sanitize_string(self, string: str) -> str:
        """Function that sanitizes a string
        It will limit the string to 1024 chars and strip it
        Args:
            string (str): unsafe string

        Returns:
            str: safe string
        """
        return string.strip()[:1024]
