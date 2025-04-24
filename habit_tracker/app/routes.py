from app import app
from flask import render_template

@app.route('/')
def home():
    print("🚀 / route hit")
    return render_template('index.html', title='Agile Web Development - Group-gc-2')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/monthly')
def monthly():
    return render_template('monthly.html')