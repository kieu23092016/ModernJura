"""store standard route for the website:
    Home Page: for guest,
    Home: for user,
    Search,
    Game"""

"blue print - include URL defined"
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Game, User
from . import db
views = Blueprint('views', __name__)
"run this function whenever go to / route"


@views.route('/', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        return redirect(url_for('views.search', search_note=search))
    return render_template("index.html")

# user------------------------------------------------------------------------
@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('logintoUser.html', user = current_user)


@views.route('/user_profile/<id>', methods=['GET', 'POST'])
def user(id):
    id = id
    user = User.query.get(id)
    return render_template("user.html", user = user)


# search------------------------------------------------------------------------

@views.route('/search', methods = ['get','post'])
def search():
    searchNote = request.args.get('search_note', None)
    print("searchNote", searchNote)
    findData = Game.query.filter(Game.gameName.contains(searchNote)).all()
    if findData:
        print("tìm thấy r :>")
    # if request.method == 'get':
    #     id = request.form('submit_button')
    id = request.form.get('gamePath')
    print('gamePath',id)
    return render_template("search.html", notes = findData, searchNote = searchNote)

@views.route('/gamePage/<id>', methods = ['get','post'])
def gamePage(id):
    id = id
    print('id', id)
    game = Game.query.get(id)
    return render_template("GamePage.html", game = game)
# info------------------------------------------------------------------------
@views.route('/admin', methods = ['get','post'])
def addInfor():
    # if request.method == "post":
    gameName = request.form.get('gameName')
    print(gameName)
    description = request.form.get('description')
    tag = request.form.get('tag')
    gameImgPath = request.form.get('gameImgPath')
    gamePath = request.form.get('gamePath')
    game = Game(gameName = gameName, description = description, tag = tag, gameImgPath = gameImgPath, gamePath=gamePath)
    db.session.add(game)
    db.session.commit()
    return render_template("admin.html")