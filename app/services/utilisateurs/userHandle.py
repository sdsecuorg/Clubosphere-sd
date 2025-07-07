"""
File containing class that handles the permission, login check of users
Uses flask-session thus not ideal for standalone unit testing
"""

from flask import session

from app.models.dataCheck import DataCheck
from app.repository.users.retrieveUsers import RetrieveUsers


class UserHandle:
    def __init__(self):
        """
        Constructor init function
        """
        self.roles = {"visitor": 0, "student": 1, "admin": 2}  # hardcoded for now

    def is_logged(self) -> dict[str, str]:
        """Function that checks if a user is logged using flask session.
        It checks the user's id then retrieves the permissions.

        Returns:
            dict[str,str]: dict containing 'status' (success if logged otherwise error), \
                            role_number (if logged otherwise 0), 'username' if logged 
        """
        if "oid" not in session:
            return {"status": "error", "role_number": self.roles["visitor"]}
        oid = str(session["oid"])
        valid_id = DataCheck().valid_mongo_id(oid)

        if not valid_id:
            return {"status": "error", "role_number": self.roles["visitor"]}

        found_user = RetrieveUsers().find_user_using_oid(oid)

        if "username" not in found_user:
            return {"status": "error", "role_number": self.roles["visitor"]}

        return {
            "status": "success",
            "role_number": found_user["role_number"],
            "username": found_user["username"],
        }

    def disconnect(self) -> None:
        session.clear()
