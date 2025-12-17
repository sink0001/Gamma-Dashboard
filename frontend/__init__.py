from flask import Flask
from backend.routes.views import views
from backend.endpoints.heartbeat_listener import heart_beat_listener

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "coolkey123"
    app.config["REDIS_HOST"] = "localhost"
    app.config["REDIS_PORT"] = 6379

    app.register_blueprint(views)
    app.register_blueprint(heart_beat_listener)
    
    return app