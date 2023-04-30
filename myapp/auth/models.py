from myapp.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='author', lazy=True)
    quizzes = db.relationship('Quiz', backref='author', lazy=True)
    participations = db.relationship('QuizParticipant', backref='participant', lazy=True)

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
        return self.user_id

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter_by(user_id=user_id).first()
        if user and user.check_password(password):
            return user
        return None