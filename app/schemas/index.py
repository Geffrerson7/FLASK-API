from app.serializer import ma
from app.models.user import User
from app.models.project import Project
from marshmallow import fields

class ProjectSchema(ma.SQLAlchemySchema):
    
    id = ma.auto_field()
    tags = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    url_image = ma.auto_field()
    url_github = ma.auto_field()
    user_id = ma.auto_field()

    class Meta:
        model = Project

class UserSchema(ma.SQLAlchemySchema):
    
    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    phone_number = ma.auto_field()
    date_born = ma.auto_field()
    last_session = ma.auto_field()
    updated_at = ma.auto_field()
    created_at = ma.auto_field()
    projects = fields.Nested(ProjectSchema, many=True)

    class Meta:
        model = User
    