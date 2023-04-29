from myapp.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
<<<<<<< HEAD
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
=======
    password_hash = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    school = db.Column(db.String(80), nullable=False)
>>>>>>> 311a7d1bd6409eab484cb5a8649cea4b7ec838c0

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
<<<<<<< HEAD
        return check_password_hash(self.password, password)
=======
        return check_password_hash(self.password_hash, password)
    
    def set_attr(self, name, school):
        self.name = name
        self.school = school
>>>>>>> 311a7d1bd6409eab484cb5a8649cea4b7ec838c0

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter_by(id=user_id).first()
        if user and user.check_password(password):
            return user
        return None
