from flask import Blueprint, session
from backend.coordinators.Cache_handler import Cache_handler
from backend.models.Stock import Stock
from flask import jsonify


stock_data = Blueprint("stock_data", __name__) # url_prefix="/stock_data/" so all endpoints have to have stock_data/ infront


def get_last_4_quarters(current_quarter: int) -> list:
    wheel = [4, 3, 2, 1, 4, 3, 2, 1]
    start_index = wheel.index(current_quarter)
    return wheel[start_index:(start_index+4)]


@stock_data.route("/graph/quarterly_ratio/<ratio>")
def quarterly_ratio_graph(ratio: str):
    stock = Stock(session["current_stock_ticker"], True)
    cache_handler = Cache_handler()
    unserialized_finances = cache_handler.get_key_value(session["session_id"])
    stock.deserialize_cached_finances(unserialized_finances)
    
    try:
        data = {}
        latest_quarter = stock.get_latest_quarter()
        last_4_quarters = get_last_4_quarters(latest_quarter)
        data["x_values"], data["y_values"] = [], []
        for i in reversed(range(4)):
            data["x_values"].append(f"Q{last_4_quarters[i]}")
            data["y_values"].append(stock.quarterly_ratio(ratio=ratio, quarter_recency=(4 - i)))
        return jsonify(success=True, data=data, error=None), 200
    except Exception as e:
        return jsonify(error=e.args[0], data=None, success=False), 400


@stock_data.route("/graph/annual_ratio/<ratio>")
def annual_ratio_graph(ratio: str):
    stock = Stock(session["current_stock_ticker"], True)
    cache_handler = Cache_handler()
    unserialized_finances = cache_handler.get_key_value(session["session_id"])
    stock.deserialize_cached_finances(unserialized_finances)

    try:
        data = {}
        latest_annum = stock.get_latest_annum()
        last_4_years = [year for year in range(latest_annum-3, latest_annum+1)] # in descending order starting with most recently available year
        data["x_values"], data["y_values"] = [], []
        for i in range(4):
            data["x_values"].append(last_4_years[i])
            data["y_values"].append(stock.annual_ratio(ratio=ratio, year=last_4_years[i]))
        return jsonify(success=True, data=data, error=None), 200
    except Exception as e:
        return jsonify(error=e.args[0], data=None, success=False), 400