"""
File containing class that handles the permission, login check of users
Uses flask-session thus not ideal for standalone unit testing
"""

import logging
from functools import wraps
from flask import session, redirect
from datetime import datetime, timezone, timedelta

from app.models.data_checks import DataCheck
from app.repository.users.retrieve_users import RetrieveUsers
from app.models.crypto import UserCrypt
from app.repository.users.modify_users import ModifyUsers
from app.models.defined_data import DefinedData


modify_users = ModifyUsers()
user_crypt = UserCrypt()
retrieve_users = RetrieveUsers()
data_check = DataCheck()
defined_data = DefinedData()


class UserHandle:
    def __init__(self):
        """
        Constructor init function
        """

    def allowed(
        self,
        logged_in: bool = False,
        visitor: bool = False,
        visitor_only: bool = False,
        above_role: int = None,
        specific_role: int = None,
    ) -> any:
        """
        Function that contains a wrapper and a decorator.
        It is applied to flask route in order to facilitate user access management.

        Args:
            logged_in (bool, optional): Allows only logged in users. Defaults to True.
            visitor (bool, optional): Allows visitors. Defaults to False.
            visitor_only (bool,optional): Allows only visitors to access. Defaults to False
            above_role (int, optional): Only allows users with a role above x. Defaults to 1.
            specific_role (int, optional): Requires users to be the specific role y. Defaults to 1.
        Returns:
            any: redirect or status | msg
        """

        def decorator(func):
            @wraps(func)
            def handle(*args, **kwargs):
                user_info = self.is_logged()
                is_logged_in = user_info["status"] == "success"
                role_number = user_info.get(
                    "role_number", defined_data.roles()["visitor"]
                )
                if visitor_only:
                    if not is_logged_in:
                        return func(*args, **kwargs)
                    return redirect("/404")

                if visitor:
                    return func(*args, **kwargs)

                if logged_in:
                    if not is_logged_in:
                        return redirect("/404")
                    return func(*args, **kwargs)

                if above_role is not None and role_number > above_role:
                    return func(*args, **kwargs)

                if specific_role is not None and role_number == specific_role:
                    return func(*args, **kwargs)

                return redirect("/404")

            return handle

        return decorator

    def apply_token(self, email: str) -> dict[str, str]:
        """Function that generates a new token,
        applies it to the user using their email as identifier,
        sets the token in the session if success
        Args:
            email (str): used to identify the user in the db

        Returns:
            dict[str,str]: status | err
        """
        token = user_crypt.gen_token()
        status = modify_users.add_new_token(token, email)
        if not status:
            return {"status": "error", "msg": "Failed to add token"}
        role = retrieve_users.find_user_using_token(token)
        session["token"] = token
        session["email"] = email
        session["role_number"] = role["role"]
        return {"status": "success"}

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
        status_apply_token = self.apply_token(email)
        if status_apply_token["status"] == "error":
            return status_apply_token

        return {"status": "success"}

    def register_user(self, email: str, password: str) -> dict[str, str]:
        """Wrapper around the register func in Register class
        This function also sets the user with a session if the register completed successfuly
        Args:
            email (str): valid email
            password (str): valid password

        Returns:
            dict[str,str]: status | err
        """
        register_status = Register().register(email, password)
        if register_status["status"] == "error":
            return register_status

        status_apply_token = self.apply_token(email)
        if status_apply_token["status"] == "error":
            return status_apply_token

        return {"status": "success"}

    def is_logged(self) -> dict[str, str]:
        """Function that checks if a user is logged using flask session.
        It checks the user's id then retrieves the permissions.

        Returns:
            dict[str,str]: dict containing 'status' (success if logged otherwise error), \
                            role_number (if logged otherwise 0), 'username' if logged 
        """
        if "token" not in session:
            return {"status": "error", "role_number": defined_data.roles()["visitor"]}
        token = str(session["token"])

        found_user = retrieve_users.find_user_using_token(token)

        if "expires_at" not in found_user:
            return {"status": "error", "role_number": defined_data.roles()["visitor"]}
        expires_at = found_user.get("expires_at")
        if not expires_at:
            return {"status": "error", "role_number": defined_data.roles()["visitor"]}

        if expires_at.tzinfo is None or expires_at.tzinfo.utcoffset(expires_at) is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        france_timezone = timezone(timedelta(hours=2))
        now = datetime.now(france_timezone)
        if expires_at < now:
            self.disconnect()
            return {"status": "error", "role_number": defined_data.roles()["visitor"]}

        return {
            "status": "success",
            "role_number": found_user["role"],
            "email": found_user["email"],
        }

    def disconnect(self) -> dict[str, str]:
        session.clear()
        if "token" in session:
            return {"status": "error", "msg": "Failed to remove the user's session."}
        return {"status": "success"}


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
        if not data_check.check_email(email):
            return {"status": "error", "msg": "Invalid email."}

        if not data_check.check_password(password):
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

        # find the user using its email

        found_user = retrieve_users.find_user_using_email(email)

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
    def data_checks(email: str, password: str) -> dict[str, str]:
        """Static function that simply checks if the
        password and email are valid and satisfying requirements.

        Args:
            email (str): email
            password (str): password

        Returns:
            dict [str,str]: status | msg
        """

        if not data_check.check_email(email):
            return {"status": "error", "msg": "Invalid email."}

        if not data_check.check_password(password):
            return {"status": "error", "msg": "Invalid password."}

        return {"status": "success"}

    def register(self, email: str, password: str) -> dict[str, str]:
        """

        Args:
            email (str): valid email with lycee-saintdenis.com domain
            password (str): valid password with over 6 in length

        Returns:
            Dict (str,str): Dict with status message (success|error) and message if error.
        """
        # Sanitize the strings
        email = data_check.sanitize_string(email)
        password = data_check.sanitize_string(password)

        # check if the username, email and passwords are valid (matching regex)
        # Return the field_checks func if the status is error
        field_checks = self.data_checks(email, password)
        if field_checks["status"] == "error":
            return field_checks

        # lookup if email and username are taken
        # don't return that email or username is taken to not facilitate data stealing
        found_email = retrieve_users.find_user_using_email(email)
        if found_email is not None:
            return {
                "status": "error",
                "msg": "Username and/or email are not available.",
            }

        # proceed to hash the password

        hashed_password = user_crypt.gen_password_hash(password)
        # prepare a dict that will be inserted into the users collection
        username = data_check.retrieve_username_from_email(email)

        if username is None:
            return {
                "status": "error",
                "msg": "Failed to get username from email address",
            }

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
