from flask import Flask

app = Flask(__name__)
@app.rout('/')
def home():
    return "Welcome to the Habit Tracker!"
