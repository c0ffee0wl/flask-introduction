#!/usr/bin/env python3

from flask_script import Manager, prompt_bool

from routes import app, db

from models import User


manager = Manager(app)


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="test1", email="test1@example.com"))
    db.session.add(User(username="test2", email="test2@example.com"))
    db.session.commit()
    print("Initialize the database.")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database.")


if __name__ == '__main__':
    manager.run()
