from app.schemas.user import UserSchema
from app.util import status
from app.models.user import UserModel

from flask_restful import (
    Resource,
    reqparse
)


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

    def get(self):
        users_shema = UserSchema(many=True)
        users = [
            user.serialize for user in UserModel.all()
        ]

        data = users_shema.dump(users)

        return data, status.HTTP_200_OK
