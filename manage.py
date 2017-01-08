#!/usr/bin/env python

from flask_script import Manager, prompt_bool

from app import app, db


manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    print("Initialize the database.")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database.")


if __name__ == '__main__':
    manager.run()
