from flask import Blueprint, session
from backend.models.Cache_handler import Cache_handler
from backend.models.Stock import Stock

stock_data = Blueprint("stock_data", __name__) # url_prefix="stock/" so all endpoints have to have stock/ infront


def get_last_4_quarters(current_quarter: int) -> list:
    wheel = [4, 3, 2, 1, 4, 3, 2, 1]
    start = current_quarter
    start_index = wheel.index(start)
    return wheel[start_index:(start_index+4)]


@stock_data.route("/graph/quarterly_ratio/<ratio>")
def graph_quarterly_ratio(ratio):
    stock = Stock(session["current_stock_ticker"], True)
    cache_handler = Cache_handler()
    unserialized_finances = cache_handler.get_key_value(session["session_id"])
    stock.deserialize_cached_finances(unserialized_finances)

    response = {}
    current_quarter = stock.get_latest_quarter()
    last_4_quarters = get_last_4_quarters(current_quarter)
    response["x_values"], response["y_values"] = [], []
    for i in range(4):
        response["x_values"].append(last_4_quarters[i])
        response["y_values"].append(stock.quarterly_ratio(ratio=ratio, quarter_recency=(4 - i)))
    
    return response