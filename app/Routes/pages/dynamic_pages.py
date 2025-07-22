"""
Required libraries
"""

from flask import render_template, Blueprint
from app.services.utilisateurs.user_handle import UserHandle
from app import limiter

dynamic_page_blueprint = Blueprint("dynamic_page", __name__)
user_handle = UserHandle()


@dynamic_page_blueprint.route("/admin/users", methods=["GET"])
@limiter.limit("3 per second")
@user_handle.allowed(logged_in=True, above_role=1)
def admin_users() -> "Render":
    """Users page

    Returns:
        Render: users.html
    """
    return render_template("/admin/users.html")


@dynamic_page_blueprint.route("/profile", methods=["GET"])
@user_handle.allowed(logged_in=True)
@limiter.limit("3 per second")
def profile() -> "Render":
    """User profile page

    Returns:
        Render: profile.html
    """
    return render_template("/profile.html")


@dynamic_page_blueprint.route("/clubs", methods=["GET"])
@limiter.limit("3 per second")
@user_handle.allowed(logged_in=True, visitor=True)
def clubs() -> "Render":
    """clubs page

    Returns:
        Render: clubs.html
    """
    return render_template("/clubs.html")
