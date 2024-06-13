# -*- encoding: utf-8 -*-

import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
# from apps.authentication.models import Users


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'tickets', 'allUsers'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
            # create_default_users() #create users
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()
            # create_default_users()
            print(initialize_database)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app

# def create_default_users():
#     admin = Users(username='admin', email='admin@gmail.com', password='admin', is_admin=True)
#     user1 = Users(username='user1', email='user1@gmail.com', password='user1', is_admin=False)
#     user2 = Users(username='user2', email='user2@gmail.com', password='user2', is_admin=False)
#     db.session.add(admin)
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.commit()
