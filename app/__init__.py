from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # provides tools for working with SQL databases in Flask applications
from flask_migrate import Migrate

from app.config.config import config_by_name


db = SQLAlchemy()


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[env_name])

    with app.app_context():
        db.session.configure(autoflush=False)
        db.init_app(app)

    migrate = Migrate(app, db)

    return app
