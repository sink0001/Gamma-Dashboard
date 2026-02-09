from flask_login import UserMixin
from backend.services import user_services


class User(UserMixin):
    def __init__(self, id: int, username: str) -> None:
        self.id = id
        self.username = username

    @classmethod
    def load_user_by_id(cls, id: int) -> User | None:
        username = user_services.get_username_by_id(id)
        if not username:
            return None
        return cls(id, username)

    def add_stock_to_watchlist(self, ticker: str) -> None:
        if user_services.ticker_already_in_user_watchlist(self.id, ticker):
            raise ValueError("This ticker is already in the watchlist")
        return user_services.add_to_user_watchlist(self.id, ticker)
    
    @property
    def watchlist(self) -> list[str]:
        return user_services.get_watchlist(self.id)