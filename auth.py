from flask import Blueprint

auth = Blueprint("auth",__name__)

@auth.route("/register")
def login():
    return "<p>email<p>"


@auth.route("/logout")
def logout():
    return "<p>logout<p>"