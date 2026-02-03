from flask import Blueprint
from backend.models.User import User


user_info = Blueprint("user_info", __name__, url_prefix="/user_info/")