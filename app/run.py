from flask import Flask
from extensions import db, migrate, api, ma
from config import Config
from resources.email import Email, EmailList
from resources.phone import Phone, PhoneList
from resources.user import User, UserList
# import generate, validators

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    api.init_app(app)

def add_apis():
    api.add_resource(Email, "/email")
    api.add_resource(EmailList, "/emails")
    api.add_resource(Phone, "/phone")
    api.add_resource(PhoneList, "/phones")
    api.add_resource(User, "/user")
    api.add_resource(UserList, "/users")

def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile('config.py')
    add_apis()

    register_extensions(app)
    return app

if __name__ == "__main__":
    app = create_app(Config)
    app.run()