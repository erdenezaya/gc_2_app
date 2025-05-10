from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):  
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)   
    habits = db.relationship('Habit', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        """Set the password hash for the user."""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        if not password:
            raise ValueError("Password cannot be empty")
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    habit_name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    records = db.relationship('HabitRecord', backref='habit', lazy=True, 
                             cascade='all, delete-orphan')
    
    

    def to_dict(self):
        from app.main.controller import get_habit_color  # ✅ lazy import to avoid circular dependency
        return {
            "id": self.id,
            "name": self.habit_name,
            "color": get_habit_color(self.id),
            "user_id": self.user_id
        }



class HabitRecord(db.Model):
    __tablename__ = 'habit_records'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)

class SharedHabit(db.Model):
    __tablename__ = 'shared_habits'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    shared_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_with = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    habit = db.relationship('Habit', backref=db.backref('shared_habits', cascade='all, delete-orphan'))
    sharer = db.relationship('User', foreign_keys=[shared_by], backref='habits_shared_by_me')
    receiver = db.relationship('User', foreign_keys=[shared_with], backref='habits_shared_with_me')