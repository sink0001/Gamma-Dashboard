from backend.repositories import user_repositories


def get_username_by_id(id: int) -> str | None:
    return user_repositories.get_username_by_id(id)


def add_to_user_watchlist(user_id: int, ticker: str) -> None:
    user_repositories.add_to_user_watchlist(user_id, ticker)


def ticker_already_in_user_watchlist(user_id: int, ticker: str) -> bool:
    return user_repositories.ticker_already_in_user_watchlist(user_id, ticker)


def get_watchlist(user_id: int) -> list[str]:
    return user_repositories.get_user_watchlist(user_id)