from flask import Flask, render_template
from app import app

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

@app.route('/logout')
def logout():
    # TODO: clear user session data
    return redirect(url_for('index'))  # redirect to homepage


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