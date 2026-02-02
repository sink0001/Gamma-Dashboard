from flask import Blueprint, request, render_template, redirect, url_for, flash
from backend.coordinators.User_gate import User_gate


auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        form = request.form
        username = form.get("username")
        password = form.get("password")
        turnstile_token = form.get("cf-turnstile-response")

        user_gate = User_gate()
        token_validity = user_gate.validate_turnstile_token(turnstile_token) # type:ignore all these form components are guaranteed to be strings since the inputs are type text
        
        username_length = len(username) # type:ignore
        password_length = len(password) # type:ignore

        if not token_validity:
            flash("We couldn't verify you are human, maybe try again?")
            return redirect(url_for("auth.signup"))
        # elif username already exists in db
        elif username_length < 1:
            flash("Enter a username")
            return redirect(url_for("auth.signup"))
        elif username_length > 255:
            flash("please enter a shorter username")
        elif password_length < 4:
            flash("password must be longer than 4 characters")
            return redirect(url_for("auth.signup"))
        elif password_length > 150:
            flash("password shorter than 150 characters")
            return redirect(url_for("auth.signup"))
        else:
            user_gate.signup_user(username, password) # type:ignore
            return redirect(url_for("views.home_page"))
        # also check whether username already exists and redirect
        return "" # placeholder for now