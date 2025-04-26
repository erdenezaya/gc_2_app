from flask import Flask, render_template, request, redirect, url_for, flash

from app import app, db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

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

from app.models import User, Habit, HabitRecord
from datetime import date

@app.route('/daily', methods=['GET', 'POST'])
def daily_habits():
    user_id = 1  # Temporary static user for now

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
        return redirect(url_for('daily_habits'))

    records = {r.habit_id: r.completed for r in HabitRecord.query.filter_by(date=today).all()}

    return render_template('daily.html', habits=habits, records=records, today=today)
@app.route('/delete_habit/<int:habit_id>')
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    # Delete all related HabitRecords first
    HabitRecord.query.filter_by(habit_id=habit.id).delete()

    db.session.delete(habit)
    db.session.commit()
    flash("Habit and related records deleted successfully")
    return redirect(url_for('daily_habits'))
@app.route('/edit_habit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if request.method == 'POST':
        new_name = request.form['habit_name']
        habit.habit_name = new_name
        db.session.commit()
        flash("Habit name updated!")
        return redirect(url_for('daily_habits'))

    return render_template('edit_habit.html', habit=habit)
