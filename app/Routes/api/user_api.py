"""
Required libraries
"""

from flask import render_template, Blueprint, request, redirect
from app.services.utilisateurs.user_handle import UserHandle
from app import limiter


users_api_blueprint = Blueprint("users_api", __name__)
user_handle = UserHandle()


@users_api_blueprint.route("/api/login", methods=["POST"])
@limiter.limit("1 per second")
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


@users_api_blueprint.route("/api/register", methods=["POST"])
@limiter.limit("1 per second")
def register() -> dict[str, str]:
    """Register API Route
    Requires :
        email (str) : valid user email
        password (str) : user's password
    Returns:
        Render: status | msg
    """
    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    return user_handle.register_user(email, password)


@users_api_blueprint.route("/api/logout", methods=["GET"])
@limiter.limit("3 per second")
def logout() -> dict[str, str] or "redirect":
    """Function that logs out the user.

    Returns:
        dict[str,str]: status | err. Redirect if success
    """
    status_disconnect = user_handle.disconnect()
    if status_disconnect["status"] == "success":
        return redirect("/login")
    return status_disconnect
