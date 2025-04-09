from flask import Flask

app = Flask(__name__)
@app.rout('/')
def home():
    return "Welcome to the Habit Tracker!"
@app.route('/habits')
def habits():
    return "Here are your habits."
@app.route('/habits/<int:habit_id>')