from flask import Flask, render_template
from app import app
from app.models import User
from datetime import date, timedelta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/dashboardtest/<username>')
def dashboardtest(username):
    user = User.query.filter_by(username=username).first_or_404()
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
    for offset in range(7):
        d = today - timedelta(days=offset)
        if all(
            any(r.date == d and r.completed for r in habit.records)
            for habit in user.habits
        ):
            streak += 1
        else:
            break  # streak must be continuous

    return render_template('dashboardtest.html', 
                           user=user, 
                           habit_stats=habit_stats,
                           today_done=todays_completed,
                           total_habits=total_habits,
                           streak_days=streak,
                           active_page='dashboard')


@app.route('/weekly')
def weekly():
    return render_template('weekly.html', active_page='weekly')

@app.route('/monthly')
def monthly():
    return render_template('monthly.html', active_page='monthly')

@app.route('/yearly')
def yearly():
    return render_template('yearly.html', active_page='yearly')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # TODO: Authenticate user
    flash("Login attempted")
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # TODO: Register user
    flash("Signup attempted")
    return redirect(url_for('index'))