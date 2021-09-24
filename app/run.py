from flask import Flask
from extensions import db, migrate, api
from config import Config
from resources.email import Email, EmailList
from resources.phone import Phone, PhoneList
from resources.user import User, UserList
import generate, validators

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    return app

if __name__ == "__main__":
    app = create_app(Config)
    app.run()