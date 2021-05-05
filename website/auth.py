"""this file include:
    login,
    sign up,
    logout,
    reset password,
    validate email of users"""

import re
import smtplib

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer

"""test validation---------------------------------------------------------------------------------------------------"""
# contains alphabets, digits and dash, from 3 to 16 characters
USERNAME_PATTERN = '^[a-z0-9_-]{3,16}$'
EMAIL_PATTERN = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
# a digit must occur at least , a lower case letter must occur at least once,
# no whitespace allowed in the entire string, from 6-10 characters
PASSWORD_PATTERN = "^(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!#%*?&]{6,10}$"

"""server send email to users----------------------------------------------------------------------------------------"""
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
EMAIL_ADDRESS = 'modernjura0503@gmail.com'
EMAIL_PASSWORD = 'modernjura03052021'
# EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

s = URLSafeTimedSerializer('Thisisasecret!')

# -----------------------------------------------------------------------------------------------------------------------

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login2.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.homePage'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))

        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif re.search(EMAIL_PATTERN, email) is None:
            flash('Email is invalid.', category='error')
        elif re.search(USERNAME_PATTERN, firstName) is None:
            flash('First name must contain alphabets, digits and dash, from 3 to 16 characters.', category='error')
        elif re.search(PASSWORD_PATTERN, password1) is None:
            flash('Password must be from 6-10 characters, have a digit must occur at least , '
                  'a lower case letter must occur at least once, no whitespace allowed in the entire string.',
                  category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            """hash - tạo hash password chỉ có thể kiểm tra password đúng bằng cách chuyển pass-> hashpass?? for what"""
            new_user = User(email=email, first_name=firstName,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('account created', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign-up.html")


@auth.route('/getEmail', methods=['GET', 'POST'])
def getEmail():
    if request.method == 'POST':
        email = request.form.get('email')
        if re.search(EMAIL_PATTERN, email) is None:
            print("email is invalid.")
        else:
            user = User.query.filter_by(email=email).first()
            # print(user)
            if user:
                # gửi email xác nhận đến người dùng-----------------------------------------------------------------------------
                # verify_code = random.randint(100001, 999999)
                # print(str(verify_code))

                token = s.dumps(email, salt='email-confirm')
                print("this is the token: " + token)
                confirm_address = "http://127.0.0.1:5000/reset_password/" + token

                message = EmailMessage()
                message['Subject'] = 'Welcome to Modern Jura!'
                message['From'] = EMAIL_ADDRESS
                message['To'] = email
                message.set_content('Please confirm your email by following links')
                message.add_alternative("""\
                        <!DOCTYPE html>
                        <html>
                            <p>
                                <a href=""" + confirm_address + """> Click here </a> to reset your password 
                            </p>
                        </html>
                        """, subtype='html')

                # message.set_content('This is your verify code.\n' + str(verify_code))

                with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(message)
                flash("We've send you a link to reset your password."
                      " This link is only active in 5 minutes. Please check your email.", category="success")
        # user = User.query.filter_by(email=email).first()
        # print(user)
        # print(email)
    return render_template("getEmail.html")


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ this function to reset password for user when user forgot """
    # this token just active in 300s
    if request.method == "POST":
        email = s.loads(token, salt='email-confirm', max_age=300)
        print(email)
        user = User.query.filter_by(email=email).first()

        newPassword1 = request.form.get('newPassword1')
        newPassword2 = request.form.get('newPassword2')

        print(user)
        if user:
            """kiểm tra password hợp lệ-chỗ này cần chỉnh thêm file html-----------------------------------------------------"""
            if re.search(PASSWORD_PATTERN, newPassword1) is None:
                flash('Password must be from 6-10 characters, have a digit must occur at least , '
                      'a lower case letter must occur at least once, no whitespace allowed in the entire string.',
                      category='error')
            elif newPassword1 != newPassword2:
                flash('Passwords don\'t match.', category='success')
            else:
                user.password = generate_password_hash(newPassword1, method='sha256')
                db.session.commit()
                print(user.password)
                print("đang thay đổi đây.............")
                flash('Change password successfully!.', category='success')
            return redirect(url_for('auth.login'))
    # ------------------------------------------------------------------------------------------------------------------
    return render_template("forgotPass.html")
