from flask import render_template
from flask_login import login_required, current_user
from . import main_bp
from app.models import User
from datetime import date, timedelta

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
    user = current_user
    today = date.today()
    start_date = today - timedelta(days=6)

    # ------- Habit-wise progress -------
    habit_stats = []
    for habit in user.habits:
        recent_records = [r for r in habit.records if start_date <= r.date <= today]
        completed_days = sum(1 for r in recent_records if r.completed)
        total_days = 7
        percentage = round((completed_days / total_days) * 100, 1)

        habit_stats.append({
            'habit_name': habit.habit_name,
            'completed_days': completed_days,
            'total_days': total_days,
            'percentage': percentage
        })

    # ------- Today’s completion -------
    todays_completed = 0
    for habit in user.habits:
        today_record = next((r for r in habit.records if r.date == today), None)
        if today_record and today_record.completed:
            todays_completed += 1
    total_habits = len(user.habits)

    # ------- Streak count -------
    streak = 0
    day_offset = 1  # start from yesterday
    while True:
        d = date.today() - timedelta(days=day_offset)

        # Check if all habits are completed for date d
        all_completed = all(
            any(r.date == d and r.completed for r in habit.records)
            for habit in user.habits
        )

        if all_completed:
            streak += 1
            day_offset += 1
        else:
            break  # break the loop once a day is missed

    return render_template('dashboard.html', 
                           user=user, 
                           habit_stats=habit_stats,
                           today_done=todays_completed,
                           total_habits=total_habits,
                           streak_days=streak,
                           active_page='dashboard')


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
