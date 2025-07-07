"""
Required libraries
"""

from flask import render_template, Blueprint


static_page_blueprint = Blueprint("static_page", __name__)


@static_page_blueprint.route("/", methods=["GET"])
def index() -> "Render":
    """Index page

    Returns:
        Render: index.html
    """
    return render_template("index.html")


@static_page_blueprint.route("/login", methods=["GET"])
def login() -> "Render":
    """
        Login page
    Returns:
        Render: login.html
    """
    return render_template("login.html")


@static_page_blueprint.route("/signin", methods=["GET"])
def signin() -> "Render":
    """
        signin page
    Returns:
        Render: signin
    """
    return render_template("signin.html")


@static_page_blueprint.route("/admin", methods=["GET"])
def admin() -> "Render":
    """
        Admin page
    Returns:
        Render: admin.html
    """
    return render_template("/admin/admin.html")


@static_page_blueprint.route("/club", methods=["GET"])
def club() -> "Render":
    """
        Club page
    Returns:
        Render: club.html
    """
    return render_template("club.html")


@static_page_blueprint.route("/about", methods=["GET"])
def about() -> "Render":
    """
        about page
    Returns:
        Render: about.html
    """
    return render_template("about.html")
