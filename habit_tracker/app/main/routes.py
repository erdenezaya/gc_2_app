from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Habit, HabitRecord, SharedSnippet, User
from datetime import datetime, timedelta
from . import main_bp

# ------------------------------------------------------------------
# Public landing page
# ------------------------------------------------------------------
@main_bp.route("/")
def home():
    """Render the landing page"""
    return render_template("index.html")

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

def get_habit_color(habit_name):
    _last_color_index = -1
    """Return the CSS color class based on habit name"""
    colors = ["green", "red", "blue", "purple"]
    _last_color_index = (_last_color_index + 1) % 4
    return colors[_last_color_index]

def calculate_streak(habit_id):
    """Calculate current streak for a habit
    
    Returns the number of consecutive days the habit has been completed
    leading up to today.
    """
    today = datetime.now().date()
    
    # Check if habit was completed today
    today_record = HabitRecord.query.filter_by(
        habit_id=habit_id,
        date=today,
        completed=True
    ).first()
    
    if not today_record:
        # Check if there's a streak that ended yesterday
        yesterday = today - timedelta(days=1)
        yesterday_record = HabitRecord.query.filter_by(
            habit_id=habit_id,
            date=yesterday,
            completed=True
        ).first()
        
        if not yesterday_record:
            return 0
        
        # Count streak days that ended yesterday
        streak = 1
        current_date = yesterday - timedelta(days=1)
    else:
        # Count streak days including today
        streak = 1
        current_date = today - timedelta(days=1)
    
    # Count consecutive days going backward
    while True:
        record = HabitRecord.query.filter_by(
            habit_id=habit_id,
            date=current_date,
            completed=True
        ).first()
        
        if not record:
            break
            
        streak += 1
        current_date -= timedelta(days=1)
    
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


# ------------------------------------------------------------------
# Auth-protected pages
# ------------------------------------------------------------------
@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard with today's habits and stats"""
    # Create default habits if user has none
    habit_count = Habit.query.filter_by(user_id=current_user.id).count()
    if habit_count == 0:
        create_default_habits(current_user.id)
    
    # Get current date
    today = datetime.now().date()
    
    # Get current user's habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    
    # Initialize habit data for the template
    habit_data = []
    total_habits = len(habits)
    completed_count = 0

    # Calculate overall streak
    streak = calculate_streak(current_user.id)
    
    # Color palette for habits
    colors = ["#34BB61", "#FF786F", "#AF75F1", "#0D99FF"]

    # For each habit, get completion status and statistics
    for habit in habits:
        # Check if habit is completed today
        today_record = HabitRecord.query.filter_by(
            habit_id=habit.id,
            date=today,
            completed=True
        ).first()
        
        is_completed = bool(today_record)
        if is_completed:
            completed_count += 1

        # Calculate streak for this habit
        habit_streak = calculate_streak(habit.id)

        # Calculate weekly completion (e.g., "6/7")
        completed_days, total_days = get_weekly_completion(habit.id)
        completion_rate = f"{completed_days}/{total_days}"

        # Get color class based on habit name
        color_class = get_habit_color(habit.habit_name)

        # Add to habit data list
        habit_data.append({
            "id": habit.id,
            "name": habit.habit_name,
            "completed": is_completed,
            "completion_rate": completion_rate,
            "completion_percent": (completed_days / total_days * 100) if total_days > 0 else 0,
            "color_class": color_class,
            "streak": habit_streak
        })

    # Calculate max streak for progress bar
    max_streak = max([h["streak"] for h in habit_data]) if habit_data else 0

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        habits=habit_data,
        completed_count=completed_count,
        total_habits=total_habits,
        max_streak=max_streak,
        streak=streak,  # user streak, not habit streak
        colors=colors
    )


@main_bp.route("/weekly")
@login_required
def weekly():
    """Render the weekly habits view"""
    # Get current user's habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    
    # Calculate date range (last 7 days)
    today = datetime.now().date()
    start_date = today - timedelta(days=6)  # 7 days including today
    
    # Format date range for display
    date_range = f"{start_date.strftime('%B %d')} - {today.strftime('%B %d')}"
    
    # Initialize habits data for the template
    habits_data = []

    # Calculate streak
    streak = calculate_streak(current_user.id)

    for habit in habits:
        # Get weekly completion data
        completed_days, total_days = get_weekly_completion(habit.id)
        completion_percentage = (completed_days / total_days * 100) if total_days > 0 else 0
        
        # Check if habit has a streak
        has_streak = calculate_streak(habit.id) >= 3  # Arbitrary threshold
        
        habits_data.append({
            "id": habit.id,
            "name": habit.habit_name,
            "completion_percentage": completion_percentage,
            "completed_days": completed_days,
            "total_days": total_days,
            "has_streak": has_streak
        })
    return render_template(
        "weekly.html",
        active_page="weekly",
        habits=habits_data,
        date_range=date_range,
        streak=streak,
    )

@main_bp.route("/monthly")
@login_required
def monthly():
    """Render the monthly habits view"""
    habit_objs = Habit.query.filter_by(user_id=current_user.id).all()

    colors = ["#48bb78", "#4299e1", "#9f7aea", "#ed8936", "#f6ad55"]

    habits = []
    for idx, h in enumerate(habit_objs):
        habits.append({
            "id": h.id,
            "name": h.habit_name,
            "color": colors[idx % len(colors)]
        })

    habit_completions = [
        {"habit_id": 1, "date": "2025-04-01", "status": "done"},
        {"habit_id": 1, "date": "2025-04-02", "status": "done"},
        {"habit_id": 2, "date": "2025-04-01", "status": "missed"},
        {"habit_id": 2, "date": "2025-04-02", "status": "done"}
    ]

    current_date = datetime.today().isoformat()
    streak = calculate_streak(current_user.id)

    return render_template(
        "monthly.html",
        active_page="monthly",
        habits=habits,
        streak=streak,
        habit_completions=habit_completions,
        current_date=current_date
    )


@main_bp.route("/yearly")
@login_required
def yearly():
    """Render the yearly habits view"""
    # Get current user's habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # Calculate streak
    streak = calculate_streak(current_user.id)

    # Color palette for habits
    colors = ["#34BB61", "#FF786F", "#AF75F1", "#0D99FF"];
    
    return render_template(
        "yearly.html",
        active_page="yearly",
        habits=habits,
        streak=streak,
        colors=colors,
    )

# ------------------------------------------------------------------
# Habit management routes
# ------------------------------------------------------------------
@main_bp.route("/habits/create", methods=["POST"])
@login_required
def create_habit():
    """Create a new habit for the current user"""
    habit_name = request.form.get("habit_name")
    
    # Validate input
    if not habit_name or not habit_name.strip():
        flash("Habit name cannot be empty", "danger")
        return redirect(url_for("main.dashboard"))
    
    # Clean input
    habit_name = habit_name.strip()
    
    # Check for duplicates
    existing = Habit.query.filter_by(
        user_id=current_user.id,
        habit_name=habit_name
    ).first()
    
    if existing:
        flash("You already have a habit with this name", "warning")
        return redirect(url_for("main.dashboard"))
    
    # Create new habit
    new_habit = Habit(
        habit_name=habit_name,
        user_id=current_user.id
    )
    
    db.session.add(new_habit)
    db.session.commit()
    
    flash(f"Habit '{habit_name}' created successfully!", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/habits/<int:habit_id>/edit", methods=["POST"])
@login_required
def edit_habit(habit_id):
    """Edit an existing habit"""
    habit = Habit.query.get_or_404(habit_id)
    
    # Verify ownership
    if habit.user_id != current_user.id:
        flash("You don't have permission to edit this habit", "danger")
        return redirect(url_for("main.dashboard"))
    
    habit_name = request.form.get("habit_name")
    
    # Validate input
    if not habit_name or not habit_name.strip():
        flash("Habit name cannot be empty", "danger")
        return redirect(url_for("main.dashboard"))
    
    # Update habit
    habit.habit_name = habit_name.strip()
    db.session.commit()
    
    flash(f"Habit updated successfully!", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/habits/<int:habit_id>/delete", methods=["POST"])
@login_required
def delete_habit(habit_id):
    """Delete a habit and all its records"""
    habit = Habit.query.get_or_404(habit_id)
    
    # Verify ownership
    if habit.user_id != current_user.id:
        flash("You don't have permission to delete this habit", "danger")
        return redirect(url_for("main.dashboard"))
    
    # Store name for confirmation message
    habit_name = habit.habit_name
    
    # Delete the habit (cascade should handle records)
    db.session.delete(habit)
    db.session.commit()
    
    flash(f"Habit '{habit_name}' deleted successfully", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/habits/<int:habit_id>/toggle", methods=["POST"])
@login_required
def toggle_habit(habit_id):
    """Toggle completion status of a habit for today"""
    habit = Habit.query.get_or_404(habit_id)
    
    # Verify ownership
    if habit.user_id != current_user.id:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        flash("You don't have permission to update this habit", "danger")
        return redirect(url_for("main.dashboard"))
    
    # Default to today if no date provided
    date_str = request.form.get("date")
    if date_str:
        try:
            record_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Invalid date format"}), 400
            flash("Invalid date format", "danger")
            return redirect(url_for("main.dashboard"))
    else:
        record_date = datetime.now().date()
    
    # Find existing record or create new one
    record = HabitRecord.query.filter_by(
        habit_id=habit_id,
        date=record_date
    ).first()
    
    if record:
        # Toggle existing record
        record.completed = not record.completed
        status_msg = "marked incomplete" if not record.completed else "marked complete"
    else:
        # Create new completed record
        record = HabitRecord(
            habit_id=habit_id,
            date=record_date,
            completed=True
        )
        db.session.add(record)
        status_msg = "marked complete"
    
    db.session.commit()
    
    # Return JSON response for AJAX requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "success": True,
            "habit_id": habit_id,
            "date": record_date.strftime("%Y-%m-%d"),
            "completed": record.completed
        })
    
    # Return to dashboard for regular form submissions
    flash(f"Habit '{habit.habit_name}' {status_msg}", "success")
    return redirect(url_for("main.dashboard"))

# ------------------------------------------------------------------
# API routes for data visualization
# ------------------------------------------------------------------
@main_bp.route("/api/habits")
@login_required
def get_habits_api():
    """Get all habits for the current user as JSON"""
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    
    result = [
        {
            "id": habit.id,
            "name": habit.habit_name
        }
        for habit in habits
    ]
    
    return jsonify(result)

@main_bp.route("/api/habits/<int:habit_id>/data")
@login_required
def get_habit_data_api(habit_id):
    """Get habit data for visualization
    
    Query parameters:
    - year: Year to get data for (default: current year)
    """
    # Verify habit belongs to current user
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Get year from query params or use current year
    year = request.args.get('year', default=datetime.now().year, type=int)
    
    # Get data for the entire year
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()
    
    records = HabitRecord.query.filter(
        HabitRecord.habit_id == habit_id,
        HabitRecord.date >= start_date,
        HabitRecord.date <= end_date
    ).all()
    
    # Format data for frontend
    result = {}
    for record in records:
        date_str = record.date.strftime('%Y-%m-%d')
        # Convert boolean to intensity level (1-4)
        # For simplicity, we'll use level 3 for completed habits
        intensity = 3 if record.completed else 0
        result[date_str] = {
            "intensity": intensity,
            "notes": ""  # We don't have notes field yet, can be added later
        }
    
    return jsonify(result)

# ------------------------------------------------------------------
# Route for sharing charts
# ------------------------------------------------------------------
@main_bp.route('/share_snippet', methods=['POST'])
@login_required
def share_snippet():
    receiver_username = request.form.get('receiver_username')
    message = request.form.get('message')

    receiver = User.query.filter_by(username=receiver_username).first()
    if not receiver:
        flash('User not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    snippet = SharedSnippet(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        message=message
    )
    db.session.add(snippet)
    db.session.commit()

    flash('Shared successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# ------------------------------------------------------------------
# Profile management page
# ------------------------------------------------------------------

@main_bp.route("/profile")
@login_required
def profile():
    """Render the user profile page"""
    # Get current user's habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()

     # Calculate streak
    streak = calculate_streak(current_user.id)
    
    return render_template(
        "profile.html",
        active_page="profile",
        user=current_user,
        database_data = db.session.query(HabitRecord).all(),
        shared_snippets = db.session.query(SharedSnippet).filter_by(receiver_id=current_user.id).all(),
        habits=habits,
        streak = streak,
    )

@main_bp.route("/update_username", methods=["POST"])
@login_required
def update_username():
    """Update the current user's username"""
    new_username = request.form.get("new_username").strip()
    
    if not new_username:
        flash("Username cannot be empty", "danger")
        return redirect(url_for("main.profile"))
    
    # Check if username is already taken
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        flash("This username is already taken", "warning")
        return redirect(url_for("main.profile"))
    
    # Update username
    current_user.username = new_username
    db.session.commit()
    flash("Username updated successfully!", "success")
    return redirect(url_for("main.profile"))

@main_bp.route("/update_email", methods=["POST"])
@login_required
def update_email():
    """Update the current user's email"""
    new_email = request.form.get("new_email").strip()
    
    if not new_email:
        flash("Email cannot be empty", "danger")
        return redirect(url_for("main.profile"))
    
    # Check if email is already taken
    existing_user = User.query.filter_by(email=new_email).first()
    if existing_user:
        flash("This email is already in use", "warning")
        return redirect(url_for("main.profile"))
    
    # Update email
    current_user.email = new_email
    db.session.commit()
    flash("Email updated successfully!", "success")
    return redirect(url_for("main.profile"))

@main_bp.route("/update_password", methods=["POST"])
@login_required
def update_password():
    """Update the current user's password"""
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    
    if not current_password or not new_password:
        flash("All fields are required", "profile_error")
        return redirect(url_for("main.profile"))
    
    # Verify current password
    if not current_user.check_password(current_password):
        flash("Current password is incorrect", "profile_error")
        return redirect(url_for("main.profile"))
    
    # Update password
    current_user.set_password(new_password)
    db.session.commit()
    flash("Password updated successfully!", "profile")
    return redirect(url_for("main.profile"))