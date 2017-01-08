import os
from datetime import datetime
# from logging import DEBUG

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from forms import BookmarkForm
import models


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/thermos'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'thermos.db')
# app.logger.setLevel(DEBUG)

# If a secret key is set, cryptographic components can use this to sign cookies and other things.
# Set this to a complex random value when you want to use the secure cookie for instance.
# import os; os.urandom(24)
app.secret_key = b"\xa4\x97\x05T9\x11B\xd3@\x89\xa3\xa7\x0e\xde(NA\xb17I&X\xde'"

db = SQLAlchemy(app)


# For bootstrap: Flask-Bootstrap extension on PyPI

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", new_bookmarks=models.Bookmark.newest(5))


@app.route("/add", methods=["GET", "POST"])
def add():

    form = BookmarkForm()

    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        # app.logger.debug("Stored url: " + url)
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for("index"))

    return render_template("add.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 400


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)
