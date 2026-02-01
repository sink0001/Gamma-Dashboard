from flask import Flask
from backend.routes.views import views
from backend.endpoints.heartbeat_listener import heart_beat_listener
from backend.endpoints.stock_data import stock_data
from backend.routes.auth import auth
from psycopg_pool import ConnectionPool
import os
from dotenv import find_dotenv, load_dotenv


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "coolkey123"
    app.config["REDIS_HOST"] = "localhost"
    app.config["REDIS_PORT"] = 6379

    app.register_blueprint(views)
    app.register_blueprint(heart_beat_listener)
    app.register_blueprint(stock_data, url_prefix="/stock_data/")
    app.register_blueprint(auth, url_prefix="/auth/")
    
    app.pg_connection_pool = ConnectionPool(f"host=localhost dbname=postgres user=postgres port=5432 password={POSTGRES_PASSWORD}", min_size=4, max_size=10) # type:ignore
    
    return app