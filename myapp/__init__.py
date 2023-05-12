from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO, send, emit, disconnect
import eventlet


def create_app():
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
        return User.get(user_id)

    from myapp.views import auth
    from myapp.utils import streamer

    auth.init_auth_routes(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    streamer.init_stream_socket(socketio)

    return (app, socketio)
