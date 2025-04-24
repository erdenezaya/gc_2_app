from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'))
app.config.from_object(Config)   # Load the configuration from the Config class
db = SQLAlchemy(app)             # Initialize the database
migrate = Migrate(app, db)       # Initialize the migration tool

<<<<<<< HEAD
from app import routes, models
=======
# You can configure your app here
# app.config['SECRET_KEY'] = 'your_secret_key'

# Import your routes after app is initialized
from app import routes

@app.route('/yearly')
def login():
    return render_template('yearly.html')
>>>>>>> dev
