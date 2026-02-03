from flask_login import UserMixin
from backend.services import auth_services


class User(UserMixin):
    def __init__(self, id: int, username: str) -> None:
        self.id = id
        self.username = username

    @classmethod
    def load_user_by_id(cls, id: int) -> User:
        username = auth_services.get_username_by_id(id)
        return cls(id, username)