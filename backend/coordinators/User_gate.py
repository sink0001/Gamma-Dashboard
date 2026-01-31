from backend.services import auth_services


class User_gate:
    def validate_turnstile_token(self, token: str) -> dict:
        return auth_services.validate_turnstile_token(token)