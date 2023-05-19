import pytest
from flask import Flask, session
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer, QuizQuestion
from myapp.database.db import db
from flask_sqlalchemy import SQLAlchemy
import os
from myapp import create_app


@pytest.fixture
def app():
    # Create a Flask app for testing
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'instance', 'quizzes.db'
    )
    app.config['SECRET_KEY'] = 'test_secret_key'
    db = SQLAlchemy(app)
    return app


@pytest.fixture
def client():
    app, _ = create_app()
    with app.test_client() as client:
        with app.app_context():
            # Check if the user already exists
            existing_user = User.query.filter_by(user_id='testuser').first()
            if not existing_user:
                # Create and commit necessary test data to the database
                user = User(user_id='testuser', name='Test User',
                            school='Test School')
                user.set_password('testpassword')
                db.session.add(user)
                db.session.commit()
        yield client


def test_login(client):
    response = client.post(
        '/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logged in as: testuser' in response.data


def test_login_invalid_credentials(client):
    response = client.post(
        '/login', data={'username': 'testuser', 'password': 'wrongpassword'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data


def test_logout(client):
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'Logged in as:' not in response.data


def test_register(client):
    response = client.post('/register', data={'name': 'Test User', 'school': 'Test School',
                           'username': 'newuser', 'password': 'newpassword'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please login' in response.data


def test_register_existing_user(client):
    response = client.post('/register', data={'name': 'Test User', 'school': 'Test School',
                           'username': 'testuser', 'password': 'newpassword'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'A user with that username already exists' in response.data


def test_create_quiz(client):
    with client.session_transaction() as session:
        session['user_id'] = 'testuser'

    response = client.post(
        '/create', data={'title': 'Test Quiz'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Test Quiz' in response.data


# Add more test cases to cover other routes and functionalities


if __name__ == '__main__':
    pytest.main()
