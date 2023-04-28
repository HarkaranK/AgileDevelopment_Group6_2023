<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from myapp.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
=======
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
class User:
    users = {'user1': {'password': 'password1', 'type': 'professor'}, 'user2': {'password': 'password2', 'type': 'student'}}

    def __init__(self, id):
        self.id = id
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.get(user_id)
        if user is None or not user.check_password(password):
            return None
        return user
=======
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
    @classmethod
    def get(cls, user_id):
        if user_id not in cls.users:
            return None
        return cls(user_id)

    @classmethod
    def authenticate(cls, user_id, password):
        if user_id not in cls.users or cls.users[user_id]['password'] != password:
            return None
        return cls(user_id)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
