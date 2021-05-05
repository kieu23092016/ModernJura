"""store standard route for the website:
    Home Page: for guest,
    Home: for user,
    Search,
    Game"""

"blue print - include URL defined"
from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)
"run this function whenever go to / route"


@views.route('/', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        if search != None:
            return redirect(url_for('views.search'))
    return render_template("index.html")


@views.route('/search')
def search():
    return render_template("search.html")


# user------------------------------------------------------------------------
@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('user_home.html')


@views.route('/user_profile', methods=['GET', 'POST'])
def user():
    return render_template("user.html")


@views.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("settings.html")


# link to our games ----------------------------------------------------------
@views.route('/SnakePage')
def snakePage():
    return render_template("SnakePage.html")


@views.route('/SnakePlay')
def snakePlay():
    return render_template("Snake.html")
