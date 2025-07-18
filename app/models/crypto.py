"""
Cryptography file containing crypto classes used by the app.
"""

import secrets
from werkzeug.security import generate_password_hash, check_password_hash


class UserCrypt:

    def __init__(self):
        self.salt_length = 32

    def gen_token(self):
        """Function used to generate a token
        Returns:
            str: token
        """
        return secrets.token_urlsafe(self.salt_length)

    def gen_password_hash(self, password: str) -> str:
        """Function used to generate a password hash
        It is essentially a wrapper around the
                    werkzeug.security.generate_password_hash()

        Args:
            password (str): plain password

        Returns:
            str: hashed password
        """
        return generate_password_hash(str(password), salt_length=self.salt_length)

    def check_password_against_hash(self, password: str, hashed_password: str) -> bool:
        """Function that checks a plain password against a hashed password.


        Args:
            password (str): plain user password
            hashed_password (str): hashed password

        Returns:
            bool: True if the hash password corresponds to the plain password.
                False otherwise
        """
        return check_password_hash(hashed_password, password)
