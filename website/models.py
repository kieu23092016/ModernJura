from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    userName = db.Column(db.String(150), unique=True)
    dateOfBirth = db.Column(db.Date)
    country = db.Column(db.String(100))
    sex = db.Column(db.String(15))  # giới tính là nam, nữ, không muốn nói
    # avatar = db.Column(db.engine)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameName = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    gamePath = db.Column(db.String(2000), unique=True)
    # tag = db.Column(db.String(100))
    # introVideo = db.Column()
    # picture = db.Column()


# class Favorite(db.Model):
#     userID = db.Column(db.Integer, db.ForeignKey('userID'))
#     gameID = db.Column(db.Integer, db.ForeignKey('gameID'))


# class Player(db.Model):
#     playerID = db.Column(db.Integer, db.ForeignKey('playerID'))
#     gameID = db.Column(db.Integer, db.ForeignKey('gameID'))
#     max_point = db.Column(db.Integer)


# class Comment(db.Model):
#     gameID = db.Column(db.Integer, db.ForeignKey('gameID'))
#     userID = db.Column(db.Integer, db.ForeignKey('userID'))
#     added_date = db.Column(db.DateTime)