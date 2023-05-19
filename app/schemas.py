from app.serializer import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    phone_number = ma.auto_field()
    date_born = ma.auto_field()
    last_session = ma.auto_field()
    updated_at = ma.auto_field()
    created_at = ma.auto_field()
