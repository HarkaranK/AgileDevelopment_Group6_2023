import pytest
from flask import Flask, session
from myapp.auth.models import User
from myapp.database.models import Quiz, Question, Answer, QuizQuestion
from myapp.database.db import db
from flask_sqlalchemy import SQLAlchemy
import os
from myapp import create_app

@pytest.fixture
def client():
    """
    Fixture that provides a Flask test client for use in tests.
    
    The fixture creates an application context, commits necessary test data to the database, and provides the client.
    The client allows sending requests to the application without running the server.
    
    Yields:
        FlaskClient: A test client instance for the Flask application.
    """
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

def test_logout(client):
    """
    Test for the logout endpoint.

    Checks whether a successful logout redirects properly and 
    whether the 'Logged in as:' text is not in the response data, 
    indicating the user is not logged in.

    Args:
        client (FlaskClient): The test client used to make requests to the app.
    """
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'Logged in as:' not in response.data

def test_create_quiz(client):
    """
    Test for the create quiz endpoint.

    Sets a 'user_id' in the session to mimic a logged in user and sends a POST request to create a quiz.
    Checks whether the request is successful and whether the new quiz title appears in the response data.

    Args:
        client (FlaskClient): The test client used to make requests to the app.
    """
    with client.session_transaction() as session:
        session['user_id'] = 'testuser'

    response = client.post(
        '/create', data={'title': 'Test Quiz'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Test Quiz' in response.data

if __name__ == '__main__':
    pytest.main()
