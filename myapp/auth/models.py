class User:
    users = {'user1': {'password': 'password1', 'type': 'professor'}, 'user2': {'password': 'password2', 'type': 'student'}}

    def __init__(self, id):
        self.id = id

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
        if user_id not in cls.users:
            return None
        return cls(user_id)

    @classmethod
    def authenticate(cls, user_id, password):
        if user_id not in cls.users or cls.users[user_id]['password'] != password:
            return None
        return cls(user_id)
