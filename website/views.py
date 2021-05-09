"""store standard route for the website:
    Home Page: for guest,
    Home: for user,
    Search,
    Game"""

"blue print - include URL defined"
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Game, User, Comment
from . import db
import os, re
views = Blueprint('views', __name__)
"run this function whenever go to / route"


@views.route('/', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        return redirect(url_for('views.search', search_note=search))
    return render_template("index.html", user = current_user)

# user------------------------------------------------------------------------
@views.route('/user_profile/<id>', methods=['GET', 'POST'])
def user(id):
    id = id
    user = User.query.get(id)
    return render_template("user.html", user = user)

#
# @views.route('/settings/<id>', methods=['GET', 'POST'])
# def settings(id):
#     user = User.query.get(id)
#     return render_template("settings.html", user = user)

# search------------------------------------------------------------------------
@views.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("settings.html")


@views.route('/upload_avatar', methods=['GET', 'POST'])
def upload_avatar():
    if request.method == 'POST':
        target = os.path.join(VIEW_ROOT, 'static\\images\\user_avatars')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print('couldn\'t create upload directory: {}'.format(target))
        upload_a = request.files.get('file')
        print("{} is the file name".format(upload_a.filename))
        # match dùng để kiểm tra tệp có hợp lệ không
        match = ["image/jpeg", "image/png", "image/jpg", "image/gif"]
        filetype = upload_a.content_type
        # print("Đây là loại của tệp nhaaaaaaaaaaaaaaaaaaaaaaaaa: ", filetype)
        if not ((filetype == match[0]) or (filetype == match[1]) or (filetype == match[2]) or (filetype == match[3])):
            return "------------------wrong type----------------"
        else:
            player = User.query.filter_by(id=1).first()
            avt_name = "user" + str(player.id) + ".jpg"
            destination = "/".join([target, avt_name])
            # lưu ảnh vào folder đã chọn
            upload_a.save(destination)
            # lưu ảnh vào cơ sở dữ liệu
            player.avatar_image = avt_name
            db.session.commit()
            return "this file upload successfully!"
    return render_template('temp_uploadImage.html')

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
    comment = request.form.get('comment')
    print("comment",comment)
    newComment = Comment(commentContent = comment)
    db.session.add(newComment)
    db.session.commit()
    return render_template("GamePage.html", game = game, user = current_user, newComment = newComment)
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