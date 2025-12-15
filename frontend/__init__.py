from flask import Flask, Blueprint
from backend.routes.views import views
from backend.endpoints.heartbeat_listener import heart_beat_listener

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "coolkey123"
    app.config["SESSION_COOKIE_HTTPONLY"] = False

    app.register_blueprint(views)
    app.register_blueprint(heart_beat_listener)
    
    return app