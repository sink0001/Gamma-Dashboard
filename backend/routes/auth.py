from flask import Blueprint, request, render_template, redirect, url_for, flash


auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        turnstile_token = request.form.get("cf-turnstile-response")
        if len(username) < 1: # type:ignore
            flash("Enter a username")
            return redirect(url_for("auth.signup"))
        elif len(password) < 4: # type:ignore
            flash("password must be longer than 4 characters")
            return redirect(url_for("auth.signup"))
        # also check whether username already exists and redirect
        return "" # placeholder for now