
# Create database initially with

# python3
# from routes import db
# from models import User, Bookmark
# db.create_all()
# u=User(username="soandso", email="info@example.com")
# db.session.add(u)
# db.session.commit()

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


db = SQLAlchemy()


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    def __repr__(self):
        return "<Bookmark '{}': '{}'".format(self.description, self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    # First argument gives many side of the relation
    # backref is the name of an attribute on the related object / that will be set on the many side
    bookmarks = db.relationship("Bookmark", backref="user", lazy="dynamic")

    def __repr__(self):
        return "<User %r>" % self.username
