import os
# from logging import DEBUG

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from models import db
from forms import BookmarkForm, LoginForm, SignupForm
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
login_manager.login_view = "login"
login_manager.init_app(app)


# For bootstrap: Flask-Bootstrap extension on PyPI

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


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
        bm = Bookmark(user=current_user, url=url, description=description)
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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user',
                                                username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password= form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
