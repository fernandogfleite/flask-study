from app.schemas.user import UserSchema
from app.util import status
from app.models.user import UserModel
from app import jwt

from flask import jsonify
from flask_restful import (
    Resource,
    reqparse
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user
)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )

    def post(self):
        user_shema = UserSchema()
        data = User.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                'message': 'This username is already be taken'
            }, status.HTTP_400_BAD_REQUEST

        user = UserModel(**data)
        user.save_to_db()

        data = user_shema.dump(user)

        return data, status.HTTP_201_CREATED

    @jwt_required()
    def get(self):
        print(current_user)
        users_shema = UserSchema(many=True)
        users = [
            user.serialize for user in UserModel.all()
        ]

        data = users_shema.dump(users)

        return data, status.HTTP_200_OK


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )

    def post(self):
        data = User.parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {
                'message': 'Wrong username or password.'
            }, status.HTTP_401_UNAUTHORIZED
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
