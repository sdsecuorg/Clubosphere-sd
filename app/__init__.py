"""
`__init__`file that contains functions such as create_app which are required to start the flask app
"""

from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from flask_limiter import Limiter
import secrets

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
    # limiter.init_app(app)

    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.secret_key = secrets.token_hex(32)

    @app.errorhandler(404)
    def page_not_found(e: Exception) -> tuple():
        """RETURN 404 page error"""
        return render_template("status/404.html", reason=e), 404

    @app.errorhandler(500)
    def internal_server_error(e: Exception) -> tuple():
        """Return 500 error page"""
        return render_template("status/500.html", reason=e), 500

    from .Routes.pages.dynamicPages import dynamic_page_blueprint
    from .Routes.pages.staticPages import static_page_blueprint

    app.register_blueprint(dynamic_page_blueprint)
    app.register_blueprint(static_page_blueprint)

    return app
