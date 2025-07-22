"""
File containing classes used to verify data
"""

import re
import unicodedata
import html
from bson.objectid import ObjectId


class DataCheck:
    """
    Class used to verify data such as username, passwords ,email ..
    """

    @staticmethod
    def check_username(username: str) -> bool:
        """Check whether the username is valid.

        Args:
            username (str): username to verify

        Returns:
            bool: True if username is valid. Otherwise False.
        """
        pattern = re.compile(r"^[a-zA-Z0-9_]{3,30}$")
        return bool(pattern.match(username))

    @staticmethod
    def check_email(email: str) -> bool:
        """Function used to check the regex of emails

        Args:
            email (str): email string

        Returns:
            bool : True if valid otherwise False.
        """
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@lycee-saintdenis\.com$")
        return bool(pattern.match(email))

    @staticmethod
    def check_password(password: str) -> bool:
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

    @staticmethod
    def valid_mongo_id(oid: str) -> bool:
        """Function that checks if the oid is valid

        Args:
            oid (str): oid string

        Returns:
            bool: True if valid otherwise False.
        """
        return ObjectId.is_valid(oid)

    @staticmethod
    def sanitize_string(string: str) -> str:
        """Function that sanitizes a string by

            - Normalizing Unicode
            - Stripping whitespace
            - Limiting to 1024 characters
            - Removing control characters
            - Escaping HTML

        Args:
            string (str): unsafe string

        Returns:
            str: safe string
        """
        if not isinstance(string, str):
            return ""
        string = unicodedata.normalize("NFKC", string)
        string = string.strip()[:1024]
        string = re.sub(r"[^\x20-\x7E\n\t]", "", string)
        string = html.escape(string)
        return string

    @staticmethod
    def retrieve_username_from_email(email: str) -> str | None:
        """Function that retrieves the username from an email address
        it retrives the part before the @domain.tld

        Args:
            email (str): user email

        Returns:
            str : username string OR None if pattern is not found
        """
        pattern = r"^(.*?)@lycee-saintdenis\.com$"
        match = re.match(pattern, email)
        if match:
            return match.group(1)
        else:
            return None
