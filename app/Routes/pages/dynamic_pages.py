"""
Required libraries
"""

from flask import render_template, Blueprint

from app import limiter

dynamic_page_blueprint = Blueprint("dynamic_page", __name__)


@dynamic_page_blueprint.route("/admin/users", methods=["GET"])
@limiter.limit("3 per second")
def admin_users() -> "Render":
    """Users page

    Returns:
        Render: users.html
    """
    return render_template("/admin/users.html")
