"""
Required libraries
"""

from flask import render_template, Blueprint
from app import limiter

static_page_blueprint = Blueprint("static_page", __name__)


@static_page_blueprint.route("/", methods=["GET"])
@limiter.limit("5 per second")
def index() -> "Render":
    """Index page

    Returns:
        Render: index.html
    """
    return render_template("index.html")


@static_page_blueprint.route("/login", methods=["GET"])
@limiter.limit("5 per second")
def login() -> "Render":
    """
        Login page
    Returns:
        Render: login.html
    """
    return render_template("login.html")


@static_page_blueprint.route("/signin", methods=["GET"])
@limiter.limit("5 per second")
def signin() -> "Render":
    """
        signin page
    Returns:
        Render: signin
    """
    return render_template("signin.html")


@static_page_blueprint.route("/admin", methods=["GET"])
@limiter.limit("5 per second")
def admin() -> "Render":
    """
        Admin page
    Returns:
        Render: admin.html
    """
    return render_template("/admin/admin.html")


@static_page_blueprint.route("/about", methods=["GET"])
@limiter.limit("5 per second")
def about() -> "Render":
    """
        about page
    Returns:
        Render: about.html
    """
    return render_template("about.html")
