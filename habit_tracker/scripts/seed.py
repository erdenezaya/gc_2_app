import os, sys

# 1) ensure the habit_tracker/ directory is on the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Habit

# Create the application instance
app = create_app()

with app.app_context():
    db.create_all()

    # Initial user for starting the app
    # This user will be used to log in and create the first habit

    username = os.getenv("SEED_USERNAME", "test")
    email = os.getenv("SEED_EMAIL", "test@test.com")
    password = os.getenv("SEED_PASSWORD", "test123")

    seed_user = User.query.filter_by(username=username).first()
    if not seed_user:
        seed_user = User(username=username, email=email)
        seed_user.set_password(password)
        db.session.add(seed_user)
        db.session.commit()
        print(f"Added seed user: {username}")
    else:
        print(f"Seed user {username} already exists. Skipping creation.")

    habits = ["Drink Water", "Read", "Mindfulness", "Exercise", "Sleep Well"]
    added = 0

    for name in habits:
        exists = Habit.query.filter_by(habit_name=name, user_id=seed_user.id).first()
        if not exists:
            habit = Habit(habit_name=name, user_id=seed_user.id)
            db.session.add(habit)
            added += 1
        else:
            print(f"Habit '{name}' already exists for user {username}. Skipping creation.")
    
    if added > 0:
        db.session.commit()
        print(f"Added {added} seed habits for user {username}.")
    else:
        print(f"No new habits added for user {username}. All habits already exist.")