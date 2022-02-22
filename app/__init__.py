from config import Config

from flask import Flask
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def init_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY

    api = Api(app)

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from app.resources.user import User
        api.add_resource(User, '/users')
        db.create_all()

        return app
