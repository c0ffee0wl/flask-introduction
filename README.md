# Create database initially with

`python3
from routes import db
from models import User, Bookmark
db.create_all()
u=User(username="soandso", email="info@example.com")
db.session.add(u)
db.session.commit()`