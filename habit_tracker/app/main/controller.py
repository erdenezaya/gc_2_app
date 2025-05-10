from app.models import Habit, HabitRecord, User
from datetime import datetime, timedelta
# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def create_default_habits(user_id):
    """Create default habits for new users"""
    # Default habit names
    default_habits = [
        "Wake up early",
        "Drink water",
        "No takeout",
        "Meditate"
    ]
    
    # Check if user already has habits
    existing_count = Habit.query.filter_by(user_id=user_id).count()
    if existing_count > 0:
        return  # User already has habits
    
    # Create default habits
    for habit_name in default_habits:
        habit = Habit(
            habit_name=habit_name,
            user_id=user_id
        )
        db.session.add(habit)
    
    db.session.commit()

# Assign color deterministically based on habit ID
COLOR_PALETTE = [
    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
    "#9966FF", "#FF9F40", "#00C49F", "#FF4444"
]

def get_habit_color(habit_id):
    return COLOR_PALETTE[habit_id % len(COLOR_PALETTE)]


def calculate_streak(user_id):
    """Calculate current streak for a user based on all habits being completed.

    Returns the number of consecutive days all habits were completed, starting from yesterday.
    """
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
   
    # Check if all habits for the user are completed today
    habits = Habit.query.filter_by(user_id=user_id).all()
    all_completed_today = all(
        HabitRecord.query.filter_by(
            habit_id=habit.id,
            date=today,
            completed=True
        ).first()
        for habit in habits
    )
    
    streak = 1 if all_completed_today else 0

    # Start streak calculation from yesterday
    current_date = yesterday

    while True:
        # Check if all habits for the user were completed on the current date
        habits = Habit.query.filter_by(user_id=user_id).all()
        all_completed = all(
            HabitRecord.query.filter_by(
                habit_id=habit.id,
                date=current_date,
                completed=True
            ).first()
            for habit in habits
        )
        
        if not all_completed:
            break  # Streak ends if any habit is not completed on the current date
        
        streak += 1
        current_date -= timedelta(days=1)  # Move to the previous day

    return streak

def get_weekly_completion(habit_id):
    """Get weekly completion data for a habit
    
    Returns tuple: (completed_days, total_days)
    """
    today = datetime.now().date()
    start_date = today - timedelta(days=6)  # Last 7 days including today
    
    # Get all habit records in date range
    records = HabitRecord.query.filter(
        HabitRecord.habit_id == habit_id,
        HabitRecord.date >= start_date,
        HabitRecord.date <= today,
        HabitRecord.completed == True
    ).all()
    
    completed_days = len(records)
    total_days = 7  # Last 7 days
    
    return (completed_days, total_days)