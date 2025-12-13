from flask import Blueprint, render_template, request


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        return render_template("base.html")
    else:
        # do the logic for determining whether the stock exists or not and if it does store its ticker in session and display the stocks info
        return render_template("stock-analysis.html")