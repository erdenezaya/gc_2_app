from flask import Blueprint

"""
Main blueprint – public pages, dashboard, habits, etc.
"""

main_bp = Blueprint(
    "main",
    __name__,
    template_folder="templates"
)

from . import routes            # noqa: E402