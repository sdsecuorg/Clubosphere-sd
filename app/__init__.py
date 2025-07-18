"""
`__init__`file that contains functions such as create_app which are required to start the flask app
"""

import secrets
import os
import logging
from dotenv import load_dotenv
from colorama import Fore, Style, init
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

csrf = CSRFProtect()
init(autoreset=True)
load_dotenv()
limiter = Limiter(storage_uri=os.getenv("MONGO_URI"), key_func=get_remote_address)


class CustomFormatter(logging.Formatter):
    """Custom formatter to add colors based on log levels."""

    def format(self, record: {}) -> str:
        """Custom format for logging with colorama"""
        base_fmt = (
            f"{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - %(levelname)s - %(message)s"
        )
        color_map = {
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
        }

        level_color = color_map.get(record.levelno, Fore.YELLOW)
        log_fmt = base_fmt.replace(
            "%(levelname)s", f"{level_color}%(levelname)s{Style.RESET_ALL}"
        )
        setup_logging()
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_app():
    app = Flask(__name__)
    _self = "self"
    Talisman(
        app,
        content_security_policy={
            "default-src": _self,
            "img-src": "*",
            "script-src": [
                _self,
            ],
            "style-src": "*",
            "font-src": ["fonts.gstatic.com"],
        },
        content_security_policy_nonce_in=["script-src"],
        feature_policy={
            "geolocation": "'none'",
        },
    )
    csrf.init_app(app)
    limiter.init_app(app)

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


def setup_logging() -> None:
    """Logger"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger("pymongo").setLevel(logging.WARNING)

    formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
