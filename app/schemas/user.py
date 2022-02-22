from app.models.user import UserModel
from app import ma


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id = ma.auto_field()
    username = ma.auto_field()
