from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from backend.coordinators.User_gate import User_gate
from backend.models.User import User


auth = Blueprint("auth", __name__, url_prefix="/auth/")


def check_credential_format(username: str, password: str, turnstile_token_validity: bool) -> bool:
    username_length = len(username) # type:ignore
    password_length = len(password) # type:ignore
    if not turnstile_token_validity:
        flash("We couldn't verify you are human, maybe try again?")
        return False
    elif username_length < 1:
        flash("Enter a username")
        return False
    elif username_length > 255:
        flash("please enter a shorter username")
        return False
    elif password_length <= 4:
        flash("password must be longer than 4 characters")
        return False
    elif password_length > 150:
        flash("password shorter than 150 characters")
        return False
    return True


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
        if check_credential_format(username, password, token_validity): # type:ignore
            success = user_gate.signup_user(username, password) # type:ignore
            if not success:
                flash("a user with that username already exists")
                return redirect(url_for("auth.signup"))
            user_id = user_gate.get_id_by_username(username) # type:ignore
            user = User(user_id, username) # type:ignore
            login_user(user)
            return redirect(url_for("views.home_page"))
        return redirect(url_for("auth.signup"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = request.form
        username = form.get("username")
        password = form.get("password")
        turnstile_token = form.get("cf-turnstile-response")

        user_gate = User_gate()
        token_validity = user_gate.validate_turnstile_token(turnstile_token) # type:ignore
        if check_credential_format(username, password, token_validity): # type:ignore
            if user_gate.user_exists(username, password): # type:ignore
                user_id = user_gate.get_id_by_username(username) # type:ignore
                if user_id:
                    user = User(user_id, username) # type:ignore
                    login_user(user)
                return redirect(url_for("views.home_page"))
            else:
                flash("username or password is wrong")
        return redirect(url_for("auth.login"))
    

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home_page"))