from backend.services import auth_services


class User_gate:
    def validate_turnstile_token(self, token: str) -> bool:
        response = auth_services.validate_turnstile_token(token)
        return response["success"]
    
    def signup_user(self, username: str, password: str) -> bool:
        if not auth_services.username_exists(username):
            auth_services.create_user(username, password) # this also hashes the unhashed password
            return True
        return False
    
    def user_exists(self, username: str, password: str) -> bool:
        if not auth_services.username_exists(username):
            return False
        return auth_services.user_exists(username, password)
    
    def get_id_by_username(self, username: str) -> int | None:
        return auth_services.get_id_by_username(username)