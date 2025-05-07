import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    """
    Configuration class for the Flask application.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location
    SECRET_KEY = os.getenv('SECRET_KEY', 'amber_pearl_latte_is_the_best')

COLOR_PALETTE = [
    "#34BB61",  # green
    "#FF786F",  # red
    "#AF75F1",  # purple
    "#0D99FF"   # blue
]

COLOR_GRADIENTS = ["#FF786F","#AF75F1", "#0D99FF"] # red -> purple -> blue

PROGRESS_BAR_GRADIENT = ["#d4ff53", "#0D99FF"]  # lime to blue