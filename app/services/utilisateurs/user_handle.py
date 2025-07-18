"""
File containing class that handles the permission, login check of users
Uses flask-session thus not ideal for standalone unit testing
"""

import logging
from flask import session

from app.models.data_checks import DataCheck
from app.repository.users.retrieve_users import RetrieveUsers
from app.models.crypto import UserCrypt
from app.repository.users.modify_users import ModifyUsers
from app.models.defined_data import DefinedData


modify_users = ModifyUsers
user_crypt = UserCrypt
retrieve_users = RetrieveUsers()
data_check = DataCheck()
defined_data = DefinedData()


class UserHandle:
    def __init__(self):
        """
        Constructor init function
        """

    def login_user(self, email: str, password: str) -> dict[str, str]:
        """Wrapper function that calls the login func from the Login class.
        The Login class handles the data checks and db queries.
        This wrapper attributes a session cookie as well if the auth is successful.

        Args:
            email (str): user's email
            password (str): user's password

        Returns:
            dict[str,str]: status | msg
        """
        login_status = Login().login(email, password)
        if login_status["status"] == "error":
            return login_status
        # maybe add a session specific identifier ?
        session["email"] = email
        return {"status": "success"}

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
        valid_id = data_check.valid_mongo_id(oid)

        if not valid_id:
            return {"status": "error", "role_number": self.roles["visitor"]}

        found_user = retrieve_users.find_user_using_oid(oid)

        if "username" not in found_user:
            return {"status": "error", "role_number": self.roles["visitor"]}

        return {
            "status": "success",
            "role_number": found_user["role_number"],
            "username": found_user["username"],
        }

    def disconnect(self) -> None:
        session.clear()


class Login:

    @staticmethod
    def check_fields(email: str, password: str) -> dict[str, str]:
        """Function that checks the email and password fields using regex

        Args:
            email (str): email string
            password (str): password string

        Returns:
            dict[str,str]: status | err
        """
        if data_check.check_email(email):
            return {"status": "error", "msg": "Invalid email."}

        if data_check.check_password(password):
            return {"status": "error", "msg": "Invalid password."}

        return {"status": "success"}

    def login(self, email: str, password: str) -> dict[str, str]:
        """

        Args:
            email (str): valid email
            password (str): valid password with over 6 in length
        Returns:
            Dict (str,str): Dict with status message (success|error) and message if error.
        """

        # sanitize input
        email = data_check.sanitize_string(email)
        password = data_check.sanitize_string(password)

        # check validity of fields

        check_validity = self.check_fields(email, password)
        if check_validity["status"] == "error":
            return check_validity

        # find the user using its username

        found_user = retrieve_users.find_user_using_username(username)

        if found_user is None:
            return {"status": "error", "msg": "User not found"}

        # check the hashed password against the plain password

        hashed_password = found_user["password"] if "password" in found_user else None
        if hashed_password is None:
            return {"status": "error", "msg": "Failed to retrieve the user's password."}

        if not user_crypt.check_password_against_hash(password, hashed_password):
            return {"status": "error", "msg": "Incorrect password."}

        return {"status": "success"}


class Register:

    @staticmethod
    def data_checks(username: str, email: str, password: str) -> dict[str, str]:
        """Static function that simply checks if the username,
        passwords and email are valid and satisfying requirements.

        Args:
            username (str): username
            email (str): email
            password (str): password

        Returns:
            dict [str,str]: status | msg
        """
        if not data_check.check_username(username):
            return {"status": "error", "msg": "Invalid username."}

        if not data_check.check_email(email):
            return {"status": "error", "msg": "Invalid email."}

        if not data_check.check_password(password):
            return {"status": "error", "msg": "Invalid password."}

        return {"status": "success"}

    def register(self, username: str, email: str, password: str) -> dict[str, str]:
        """

        Args:
            username (str): valid username with no special chars and that is longer than 3 chars
            email (str): valid email with lycee-saintdenis.com domain
            password (str): valid password with over 6 in length

        Returns:
            Dict (str,str): Dict with status message (success|error) and message if error.
        """
        # Sanitize the strings
        username = data_check.sanitize_string(username)
        email = data_check.sanitize_string(email)
        password = data_check.sanitize_string(password)

        # check if the username, email and passwords are valid (matching regex)
        # Return the field_checks func if the status is error
        field_checks = self.data_checks(username, email, password)
        if field_checks["status"] == "error":
            return field_checks

        # lookup if email and username are taken
        # don't return that email or username is taken to not facilitate data stealing
        found_username = retrieve_users.find_user_using_username(username)
        found_email = retrieve_users.find_user_using_email(email)
        if found_username is not None or found_email is not None:
            return {
                "status": "error",
                "msg": "Username and/or email are not available.",
            }

        # proceed to hash the password

        hashed_password = user_crypt.gen_password_hash(password)
        # prepare a dict that will be inserted into the users collection
        user_role = defined_data.roles()["visitor"]
        db_document = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "role": user_role,
        }

        # insert the db_document into the users collection and check status
        status_insertion = modify_users.add_new_user(db_document)

        if status_insertion:
            return {"status": "success"}
        else:
            logging.error("Failed to add user")
            return {"status": "error", "msg": "Failed to add user"}
