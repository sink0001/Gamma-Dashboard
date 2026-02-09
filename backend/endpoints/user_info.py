from flask import Blueprint, jsonify, session
from flask_login import login_required, current_user


user_info = Blueprint("user_info", __name__, url_prefix="/user_info/")


@user_info.route("/add_ticker_to_watchlist", methods=["GET"])
@login_required
def add_to_watchlist():
    try:
        current_user.add_stock_to_watchlist(session["current_stock_ticker"]) # this raises a ValueError if the ticker is already in the 
        return jsonify(error=None, error_type=None, success=True), 200
    except Exception as e:
        return jsonify(error=e.args[0], error_type=type(e).__name__, success=False), 400