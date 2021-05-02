from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
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

        if len(email) < 4:
            flash("invalid email", category="error")
            pass
        elif len(firstName) < 4:
            flash("invalid name", category="error")
            pass
        elif password1 != password2:
            flash("password dont match", category="error")
            pass
        else:
            flash("account created", category="success")
            #add user to database
            pass

    return render_template("sign-up.html")
