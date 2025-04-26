from flask import Blueprint

"""
Authentication blueprint package.
Defines `auth_bp` and pulls in its routes.
"""

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",      # optional – only if this blueprint has its own static files
)

# Import routes after the blueprint object exists to avoid circular imports
from . import routes            # noqa: E402