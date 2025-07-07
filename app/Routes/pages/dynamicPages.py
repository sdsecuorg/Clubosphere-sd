"""
Required libraries
"""

from flask import render_template, Blueprint


dynamic_page_blueprint = Blueprint("dynamic_page", __name__)


@dynamic_page_blueprint.route("/admin/users", methods=["GET"])
def admin_users() -> "Render":
    """Users page

    Returns:
        Render: users.html
    """
    return render_template("/admin/users.html")
