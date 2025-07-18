"""
Required libraries
"""

from flask import render_template, Blueprint, request
from app.services.utilisateurs.user_handle import UserHandle


users_api_blueprint = Blueprint("users_api", __name__)
user_handle = UserHandle()


@users_api_blueprint.route("/api/login", methods=["POST"])
def login() -> dict[str, str]:
    """Login API Route
    Requires :
        email (str) : valid user email
        password (str) : user's password
    Returns:
        Render: status | msg
    """
    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    return user_handle.login_user(email, password)
