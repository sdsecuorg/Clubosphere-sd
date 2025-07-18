"""
File containing the register classes
"""

import logging

from app.models.data_checks import DataCheck
from app.models.crypto import UserCrypt
from app.models.defined_data import DefinedData
from app.repository.users.retrieve_users import RetrieveUsers
from app.repository.users.modify_users import ModifyUsers


data_check = DataCheck()
retrieve_users = RetrieveUsers()
modify_users = ModifyUsers()
user_crypt = UserCrypt()
defined_data = DefinedData()


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
