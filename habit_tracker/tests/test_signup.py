import pytest
from flask import Flask
from habit_tracker import create_app, db
from habit_tracker.models import User

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup_success(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 200
    assert b"Signup successful" in response.data

def test_signup_password_mismatch(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'confirm_password': 'password456'
    })
    assert response.status_code == 400
    assert b"Passwords do not match" in response.data

def test_signup_existing_user(client):
    # Create a user first
    client.post('/signup', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    # Try signing up with the same username
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'anotheremail@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 400
    assert b"Username already exists" in response.data

def test_signup_invalid_email(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 400
    assert b"Invalid email address" in response.data