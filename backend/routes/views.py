from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.models.Stock import Stock

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        return render_template("base.html")
    else:
        # do the logic for determining whether the stock exists or not and if it does store its ticker in session and display the stocks info
        ticker = request.form.get("searched")
        if not ticker:
            flash("Please Enter a ticker")
            return render_template("base.html")
        try:
            stock = Stock(ticker, False)
            return redirect(url_for("views.analysis_page"))
        except Exception as e:
            flash(e.args[0])
            return render_template("base.html")


@views.route("/stock-analysis")
def analysis_page():
    return render_template("stock-analysis.html")