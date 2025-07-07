"""
File containing the register classes
"""

from app.models.dataCheck import DataCheck
from app.repository.users.retrieveUsers import RetrieveUsers
from app.repository.users.modifyUsers import ModifyUsers


class Register:

    def register(
        self, username: str, email: str, password: str, password_verify: str
    ) -> dict[str, str]:
        """

        Args:
            username (str): valid username with no special chars and that is longer than 3 chars
            email (str): valid email with lycee-saintdenis.com domain
            password (str): valid password with over 6 in length
            password_verify (str): password recheck

        Returns:
            Dict (str,str): Dict with status message (success|error) and message if error.
        """

        pass
