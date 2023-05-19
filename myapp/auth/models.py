from myapp.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """User class that represents an application user.

    Args:
        user_id: A string that represents the unique identifier of the user.
        password_hash: A hashed string that represents the user's password.
        name: A string that represents the user's name.
        school: A string that represents the user's school.
        questions: A list of Question objects associated with the user.
        quizzes: A list of Quiz objects associated with the user.
        participations: A list of QuizParticipant objects associated with the user.
    """
    user_id = db.Column(db.String(36), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='author', lazy=True)
    quizzes = db.relationship('Quiz', backref='author', lazy=True)
    participations = db.relationship('QuizParticipant', backref='participant', lazy=True)

    def set_password(self, password):
        """
        Sets the user's password.
        Args:
            password (str): The password to be set for the user.
        """
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Checks the given password against the user's password.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
    
    def set_attr(self, name, school):
        """
        Sets the name and school attributes for the user.

        Args:
            name (str): The user's name.
            school (str): The user's school.
        """
        self.name = name
        self.school = school

    def is_authenticated(self):
        """
        Checks if the user is authenticated.

        Returns:
            bool: True for authenticated users as there are no unauthenticated users in this system.
        """
        return True

    def is_active(self):
        """
        Checks if the user is active.

        Returns:
            bool: True for active users as there are no inactive users in this system.
        """
        return True

    def is_anonymous(self):
        """
        Checks if the user is anonymous.

        Returns:
            bool: False for all users as there are no anonymous users in this system.
        """
        return False

    def get_id(self):
        """
        Gets the user's id.

        Returns:
            str: The user's id.
        """
        return self.user_id

    @classmethod
    def get(cls, user_id):
        """
        Retrieves a user by id.

        Args:
            user_id (str): The user's id.

        Returns:
            User: The User object with the given id, if found. Otherwise, returns None.
        """
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def authenticate(cls, user_id, password):
        """
        Authenticates a user based on id and password.

        Args:
            user_id (str): The user's id.
            password (str): The user's password.

        Returns:
            User: The User object if authentication was successful. Otherwise, returns None.
        """
        user = cls.query.filter_by(user_id=user_id).first()
        if user and user.check_password(password):
            return user
        return None