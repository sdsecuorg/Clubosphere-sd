"""
File containing predefined data fields
"""


class DefinedData:
    """Class that contains functions defining defined data fields.
    This helps with data consistency
    """

    def roles(self) -> dict[str, int]:
        """hardcoded roles for now.

        Returns:
            dict[str,int]: role dict
        """
        return {"visitor": 0, "student": 1, "admin": 2}
