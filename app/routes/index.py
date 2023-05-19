from flask import request, jsonify
from flask_smorest import Blueprint, abort
from app.models.user import User
from app.models.project import Project
from app.db import db
import bcrypt
from app.schemas.index import UserSchema, ProjectSchema
from app.utils.index import compare_password, generate_token
from datetime import datetime
from app.middlewares.index import jwt_required


projects_router = Blueprint(
    "projects_router", "projects", url_prefix="/api", description="It is an API for creating personal portfolio projects."
)


@projects_router.route("/user", methods=["GET"])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return result


@projects_router.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, message="User not found")

    user_schema = UserSchema()
    
    result = user_schema.dump(user)
    return result


@projects_router.route("/user/create", methods=["POST"])
@projects_router.response(201, UserSchema)
def add_user():
    user_schema = UserSchema()
    user_data = request.json
    password = user_data.get("password")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user_data["password"] = hashed_password

    user = user_schema.load(user_data)

    user_instance = User(**user)

    db.session.add(user_instance)
    db.session.commit()
    response_data = {
        "message": "User created successfully",
    }

    return jsonify(response_data), 201


@projects_router.route("/user/update/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, message="User not found")

    user_schema = UserSchema()
    updated_data = request.json
    password = updated_data.get("password")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    updated_data["password"] = hashed_password

    updated_user = user_schema.load(updated_data, instance=user, partial=True)

    db.session.commit()
    updated_user_data = user_schema.dump(updated_user)

    response_data = {"message": "User updated successfully", "user": updated_user_data}

    return jsonify(response_data), 200


@projects_router.route("/user/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, message="User not found")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 204


@projects_router.route("/user/login", methods=["POST"])
def login_user():
    user_schema = UserSchema()
    user_data = request.json
    password = user_data.get("password")
    email = user_data.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        abort(404, message="User does not exist!")
    else:
        password_response = compare_password(password, user.password)
        if password_response:
            user_data = user_schema.dump(user)
            token = generate_token(user_data)
            user.last_session = datetime.now()
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "User logged",
                        "token": token,
                        "last_session": user.last_session,
                    }
                ),
                201,
            )
        else:
            return abort(403, message="Incorrect password!")
        
@projects_router.route("/project", methods=["GET"])
@jwt_required
def get_projects():
    projects = Project.query.all()
    project_schema = ProjectSchema(many=True)
    result = project_schema.dump(projects)
    return result

@projects_router.route("/project/<int:id>", methods=["GET"])
@jwt_required
def get_user(id):
    project = Project.query.get(id)
    if not project:
        abort(404, message="Project not found")

    project_schema = ProjectSchema()
    
    result = project_schema.dump(project)
    return result

@projects_router.route("/project/create", methods=["POST"])
@projects_router.response(201, ProjectSchema)
@jwt_required
def add_project():
    project_schema = ProjectSchema()
    project_data = request.json
    project = project_schema.load(project_data)

    project_instance = Project(**project)

    db.session.add(project_instance)
    db.session.commit()
    
    return jsonify({"message": "Project created successfully"}), 201