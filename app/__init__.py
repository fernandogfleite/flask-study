from config import Config

from flask import Flask
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()


def init_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY

    api = Api(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.resources.user import User, Login
        api.add_resource(User, '/users')
        api.add_resource(Login, '/login')

        return app
