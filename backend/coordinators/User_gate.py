from backend.services import auth_services


class User_gate:
    def validate_turnstile_token(self, token: str) -> bool:
        response = auth_services.validate_turnstile_token(token)
        return response["success"]