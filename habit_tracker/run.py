from app import app

if __name__ == '__main__':
    app.run(debug=True)
# This will run the Flask application in debug mode, which is useful for development.
# In a production environment, you would typically use a WSGI server like Gunicorn or uWSGI to serve your Flask app.
# You can run this script from the command line to start the web application.
# Make sure to set the environment variable FLASK_APP to the name of this file before running it.
# For example, you can run:
# export FLASK_APP=run.py
# flask run

