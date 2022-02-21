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
        data = User.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                'message': 'This username is already be taken'
            }, status.HTTP_400_BAD_REQUEST

        user = UserModel(**data)
        user.save_to_db()

        return user.serialize, status.HTTP_201_CREATED

    def get(self):
        users = [
            user.serialize for user in UserModel.all()
        ]

        return users, status.HTTP_200_OK
