from flask import Flask
from backend.routes.views import views
from backend.endpoints.heartbeat_listener import heart_beat_listener
from backend.endpoints.stock_data import stock_data
from backend.endpoints.user_info import user_info
from backend.routes.auth import auth
from psycopg_pool import ConnectionPool
from os import getenv
from dotenv import find_dotenv, load_dotenv
from atexit import register
from flask_login import LoginManager


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
SECRET_KEY = getenv("FLASK_SECRET_KEY")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["REDIS_HOST"] = "localhost"
    app.config["REDIS_PORT"] = 6379

    app.register_blueprint(views)
    app.register_blueprint(heart_beat_listener)
    app.register_blueprint(stock_data)
    app.register_blueprint(auth)
    app.register_blueprint(user_info)

    pg_connection_pool = ConnectionPool(f"host=localhost dbname=gamma_dashboard_db user=postgres port=5432 password={POSTGRES_PASSWORD}", min_size=4, max_size=10)
    register(pg_connection_pool.close)
    app.pg_connection_pool = pg_connection_pool # type:ignore
    
    from backend.models.User import User
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader # this is called to check whether a user is logged in by their id and sets the current_user objects is_authenticated value accordingly
    def load_user(user_id: str) -> User | None:
        return User.load_user_by_id(int(user_id))

    return app