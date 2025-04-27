from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import main_bp
from app import db
from app.models import Habit, HabitRecord
from datetime import date

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

# ------------------------------------------------------------------
# Habit Entry & Tracking
# ------------------------------------------------------------------
@main_bp.route('/daily', methods=['GET', 'POST'])
@login_required
def daily_habits():
    user_id = 1  # Replace with current_user.id when using real user login
    habits = Habit.query.filter_by(user_id=user_id).all()
    today = date.today()

    if request.method == 'POST':
        for habit in habits:
            completed = str(habit.id) in request.form
            record = HabitRecord.query.filter_by(habit_id=habit.id, date=today).first()
            if record:
                record.completed = completed
            else:
                new_record = HabitRecord(habit_id=habit.id, date=today, completed=completed)
                db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('main_bp.daily_habits'))

    records = {r.habit_id: r.completed for r in HabitRecord.query.filter_by(date=today).all()}
    return render_template('daily.html', habits=habits, records=records, today=today)

@main_bp.route('/edit_habit/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if request.method == 'POST':
        new_name = request.form['habit_name']
        habit.habit_name = new_name
        db.session.commit()
        flash("Habit name updated!")
        return redirect(url_for('main_bp.daily_habits'))

    return render_template('edit_habit.html', habit=habit)

@main_bp.route('/delete_habit/<int:habit_id>')
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    HabitRecord.query.filter_by(habit_id=habit.id).delete()
    db.session.delete(habit)
    db.session.commit()
    flash("Habit and related records deleted successfully")
    return redirect(url_for('main_bp.daily_habits'))
