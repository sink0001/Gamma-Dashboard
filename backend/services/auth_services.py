from werkzeug.security import generate_password_hash, check_password_hash
from requests import post, RequestException
from os import getenv
from dotenv import find_dotenv, load_dotenv
from backend.repositories import user_repositories


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLOUDFLARE_TURNSTILE_SECRET_KEY = getenv("CLOUDFLARE_TURNSTILE_SECRET_KEY")


def validate_turnstile_token(token: str) -> dict:
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    data = {
        'secret': CLOUDFLARE_TURNSTILE_SECRET_KEY,
        'response': token
    }
    try:
        response = post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Turnstile validation error: {e}")
        return {'success': False, 'error-codes': ['internal-error']}


def create_user(username: str, password: str) -> None:
    hashed_password = generate_password_hash(password)
    user_repositories.create_user(username, hashed_password)


def username_exists(username: str) -> bool:
    return user_repositories.username_exists(username)


def user_exists(username: str, password: str) -> bool:
    hashed_password = user_repositories.get_username_password(username)
    return check_password_hash(hashed_password, password)


def get_username_by_id(id: int) -> str | None:
    return user_repositories.get_username_by_id(id)


def get_id_by_username(username: str) -> int | None:
    return user_repositories.get_id_by_username(username)