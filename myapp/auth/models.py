from myapp.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(120), nullable=False)  # Change the field name to password_hash
    user_type = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Update the field name here as well
        
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Update the field name here as well

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