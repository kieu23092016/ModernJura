"store stadard route for the website (ex: login page, homepage )"
"blue print - include URL defined"
from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)
"run this function whenever go to / route"
@views.route('/', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        if  search != None:
            return redirect(url_for('views.search'))
    return render_template("index.html")

@views.route('/search')
def search():
    return render_template("search.html")