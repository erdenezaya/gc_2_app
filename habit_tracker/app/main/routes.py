from flask import render_template
from flask_login import login_required
from . import main_bp

# ------------------------------------------------------------------
# Public landing page
# ------------------------------------------------------------------
@main_bp.route("/")
def home():
    return render_template("index.html")

# ------------------------------------------------------------------
# Auth-protected pages
# ------------------------------------------------------------------
@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", active_page="dashboard")


@main_bp.route("/weekly")
@login_required
def weekly():
    return render_template("weekly.html", active_page="weekly")


@main_bp.route("/monthly")
@login_required
def monthly():
    return render_template("monthly.html", active_page="monthly")


@main_bp.route("/yearly")
@login_required
def yearly():
    return render_template("yearly.html", active_page="yearly")
