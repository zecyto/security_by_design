from flask_login import UserMixin
from database.db_manager import DB_Manager

class User(UserMixin):
    _id: int
    _email: str
    _name: str

    def __init__(self, id, email = None, name = None) -> None:
        self._id = id
        self._email = email
        self._name = name

    def get_id(self):
        return self._id


