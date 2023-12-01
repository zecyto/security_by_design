from flask_login import UserMixin

class User(UserMixin):
    _id: int
    _email: str

    def __init__(self, email) -> None:
        super().__init__()
        self._email = email

