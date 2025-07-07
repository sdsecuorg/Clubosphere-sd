"""
File containing the login classes
"""

from app.models.dataCheck import DataCheck
from app.repository.users.retrieveUsers import RetrieveUsers
from app.repository.users.modifyUsers import ModifyUsers


class Login:

    def Login(self, username: str, password: str) -> dict[str, str]:
        """

        Args:
            username (str): valid username with no special chars and that is longer than 3 chars
            password (str): valid password with over 6 in length
        Returns:
            Dict (str,str): Dict with status message (success|error) and message if error.
        """

        pass
