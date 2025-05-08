import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    if SECRET_KEY is None:
        raise RuntimeError("SECRET_KEY environment variable not set! Please set it for security reasons.")

    SQLALCHEMY_DATABASE_URI = default_database_location 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

COLOR_PALETTE = [
    "#34BB61",  # green
    "#FF786F",  # red
    "#AF75F1",  # purple
    "#0D99FF"   # blue
]

COLOR_GRADIENTS = ["#FF786F","#AF75F1", "#0D99FF"] # red -> purple -> blue

PROGRESS_BAR_GRADIENT = ["#d4ff53", "#0D99FF"]  # lime to blue