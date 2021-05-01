"store stadard route for the website (ex: login page, homepage )"
"blue print - include URL defined"
from flask import Blueprint, render_template

views = Blueprint('views', __name__)
"run this function whenever go to / route"
@views.route('/')
def homePage():
    return render_template("index.html")