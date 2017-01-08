import os
# from logging import DEBUG

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required

from models import db
from forms import BookmarkForm
from models import Bookmark, User


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/thermos'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'thermos.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# If a secret key is set, cryptographic components can use this to sign cookies and other things.
# Set this to a complex random value when you want to use the secure cookie for instance.
# import os; os.urandom(24)
if os.environ.get('SECRET_KEY') is None:
    SECRET_KEY = b"\xa4\x97\x05T9\x11B\xd3@\x89\xa3\xa7\x0e\xde(NA\xb17I&X\xde'"
else:
    SECRET_KEY = os.environ['SECRET_KEY']
app.secret_key = SECRET_KEY

# app.logger.setLevel(DEBUG)
db.init_app(app)


# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)


# For bootstrap: Flask-Bootstrap extension on PyPI

# Fake login for now
def logged_in_user():
    return User.query.filter_by(username="test1").first()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", new_bookmarks=Bookmark.newest(5))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    form = BookmarkForm()

    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        # app.logger.debug("Stored url: " + url)
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for("index"))

    return render_template("add.html", form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
