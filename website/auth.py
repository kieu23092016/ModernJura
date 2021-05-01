from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)
@auth.route('/login')
def login():
    return render_template("login2.html")

@auth.route('/logout')
def logout():
    return "<p>logout<p>"

@auth.route('/sign-up')
def sign_up():
    return  "<p>sign_up<p>"