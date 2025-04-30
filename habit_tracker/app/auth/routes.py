
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User   # example model
from . import auth_bp

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('All fields are required')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('auth.signup'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('auth.signup'))
    
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        user_name = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=user_name).first()
        if not user:
            flash('User is not registered. Please sign up first.','danger')
            return redirect(url_for('main.home', show_login=True))

        if user and user.check_password(password):
            login_user(user)
            flash('Welcome!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password','danger')
            return redirect(url_for('main.home', show_login=True))
    return render_template('index.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.','info')
    return redirect(url_for('main.home', show_login=True))