
# Create database initially with

# python3
# from routes import db
# from models import User, Bookmark
# db.create_all()
# u=User(username="reindert", email="info@example.com")
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

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    def __repr__(self):
        return "<Bookmark '{}': '{}'".format(self.description, self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return "<User %r>" % self.username


# class User(object):
#     def __init__(self, firstname, lastname):
#         self.firstname = firstname
#         self.lastname = lastname
#
#     def __str__(self):
#         return "{} {}".format(self.firstname, self.lastname)
#
#     def initials(self):
#         return "{}. {}.".format(self.firstname[0], self.lastname[0])
