from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.models.Stock import Stock
from backend.models.Cache_handler import Cache_handler

views = Blueprint("views", __name__)


async def cache_searched_stocks_data(ticker: str, session_id: str, heartbeat_interval: int) -> None:
    '''
    caches a stock by caching with the session_id as the key
    and the financial statements of the key as values
    '''
    stock = Stock(ticker, True)
    cache_handler = Cache_handler()

    finances = await stock.get_finances()
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
            return render_template("base.html")
        try:
            stock = Stock(ticker, False)
            await cache_searched_stocks_data(ticker, session["session_id"], 60)
            return redirect(url_for("views.analysis_page", stock_name=ticker))
        except Exception as e:
            flash(e.args[0])
            return render_template("base.html")


@views.route("/stock-analysis/<stock_name>", methods=["GET", "POST"])
async def analysis_page(stock_name):
    if request.method == "GET": # this can only happen if the ticker exists
        print(stock_name)
        return render_template("stock-analysis.html", pe_ratio=20)
    else:
        '''
        if the ticker exists get and cache the financial statements and stuff
        so then the Stock object can calculate all the ratios by accessing cache
        '''
        ticker = request.form.get("searched")
        if not ticker:
            flash("Please enter a ticker")
            return redirect(url_for("views.home_page"))
        try:
            await cache_searched_stocks_data(ticker, session["session_id"], 60)
            return redirect(url_for("views.analysis_page", stock_name=ticker))
        except Exception as e:
            flash(e.args[0])
            return redirect(url_for("views.home_page"))
