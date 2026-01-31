from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.models.Stock import Stock
from backend.coordinators.Cache_handler import Cache_handler
from aiohttp import ClientSession


views = Blueprint("views", __name__)


async def cache_searched_stocks_data(ticker: str, session_id: str, heartbeat_interval: int) -> None:
    '''
    caches a stock by caching with the session_id as the key
    and the financial statements of the key as values
    '''
    stock = Stock(ticker, True)
    cache_handler = Cache_handler()
    
    async with ClientSession() as session:
        finances = await stock.get_finances(session)
    serialized_data = stock.serialize_finances_for_caching(finances)
    cache_handler.cache(session_id, serialized_data, heartbeat_interval)


@views.route("/", methods=["GET", "POST"])
async def home_page():
    if request.method == "GET":
        return render_template("base.html")
    else:
        # do the logic for determining whether the stock exists or not and if it does store its ticker in session and display the stocks info
        ticker = request.form.get("searched").strip() # type: ignore
        if not ticker:
            flash("Please Enter a ticker")
            return redirect(url_for("views.home_page"))
        else:
            return redirect(url_for("views.analysis_page", stock_name=ticker))


@views.route("/stock-analysis/<stock_name>", methods=["GET", "POST"])
async def analysis_page(stock_name):
    if request.method == "GET": # verify if ticker exists
        try:
            stock = Stock(stock_name, False)
            await cache_searched_stocks_data(stock_name, session["session_id"], 60)
            return render_template("stock_analysis.html", stock_name=session["current_stock_name"])
        except Exception as e:
            flash(e.args[0])
            return redirect(url_for("views.home_page"))
    else:
        ticker = request.form.get("searched")
        if not ticker:
            flash("Please enter a ticker")
            return redirect(url_for("views.home_page"))
        else:
            return redirect(url_for("views.analysis_page", stock_name=ticker))