"""
File containing the login classes
"""

from app.models.crypto import UserCrypt
from app.models.data_checks import DataCheck
from app.repository.users.retrieve_users import RetrieveUsers
from app.repository.users.modify_users import ModifyUsers

data_check = DataCheck
retrieve_users = RetrieveUsers
modify_users = ModifyUsers
user_crypt = UserCrypt


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

        if data_check.password(password):
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
