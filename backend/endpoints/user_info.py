from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.models.User import User


user_info = Blueprint("user_info", __name__, url_prefix="/user_info/")


@user_info.route("/add_ticker_to_watchlist", methods=["POST"]) # only a ticker is given in the POST body
@login_required
def add_to_watchlist():
    try:
        data = request.json
        ticker = data["ticker"] # type:ignore
        current_user.add_stock_to_watchlist(ticker)
        return jsonify(error=None, success=True), 200
    except Exception as e:
        return jsonify(error=e.args[0], success=False), 400