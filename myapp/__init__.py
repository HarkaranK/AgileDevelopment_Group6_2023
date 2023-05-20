from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO, send, emit, disconnect


def create_app():
    """
    Creates and configures a Flask application instance along with the database, login manager and socketIO server.

    Returns:
        tuple: A tuple with the Flask application instance and the socketIO instance.
    """
    app = Flask(__name__)
    app.secret_key = 'super_secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizzes.db'
    from myapp.database import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from myapp.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback function for Flask-Login that loads a user instance from a user ID.

        Args:
            user_id (str): The ID of the user to be loaded.

        Returns:
            User: The user instance, or None if the user doesn't exist.
        """
        return User.get(user_id)

    from myapp.views import auth
    from myapp.utils import streamer

    auth.init_auth_routes(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    streamer.init_stream_socket(socketio)

    return (app, socketio)
