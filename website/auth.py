from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# from werkzeug import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email = email).first()
    if user:
        if user.password == password:
            flash("loggin successful", category="success")
            return redirect(url_for('views.homePage'))
        else:
            flash("wrong password", category="error")
    else:
        flash("wrong email", category="error")
    return render_template("login2.html")

@auth.route('/logout')
def logout():
    return "<p>logout<p>"

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("email already exist", category="error")
            pass
        elif len(email) < 4:
            flash("invalid email", category="error")
            pass
        elif len(firstName) < 4:
            flash("invalid name", category="error")
            pass
        elif password1 != password2:
            flash("password dont match", category="error")
            pass
        else:
            "hash - tạo hashpassword chỉ có thể kiểm tra password đúng bằng cách chuyển pass-> hashpass?? for what "
            new_user = User(email=email, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash("account created", category="success")
            #add user to database
            return redirect(url_for('auth.login'))

    return render_template("sign-up.html")
