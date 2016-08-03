from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,userId):
        self.id = userId
    def get_id(self):
        return str(self.id)

