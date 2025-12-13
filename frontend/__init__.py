from flask import Flask, Blueprint
from backend.routes.views import views

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "coolkey123"

    app.register_blueprint(views)
    
    return app