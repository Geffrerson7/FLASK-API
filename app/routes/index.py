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
    "projects_router",
    "projects",
    url_prefix="/api",
    description="It is an API for creating personal portfolio projects. \
                 \n\nAuthor: Gefferson Casasola \
                 \nContact: gefferson.casasola@gmail.com",
)


@projects_router.route("/user", methods=["GET"])
def get_users():
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        users = User.query.paginate(page=page, per_page=per_page)
        user_schema = UserSchema(many=True)
        result = user_schema.dump(users.items)

        return {
            "data": result,
            "page": page,
            "per_page": per_page,
            "total_pages": users.pages,
            "total_items": users.total,
        }
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            abort(404, message="User not found")

        user_schema = UserSchema()

        result = user_schema.dump(user)
        return result
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/user/create", methods=["POST"])
@projects_router.response(201, UserSchema)
def add_user():
    try:
        user_schema = UserSchema()
        user_data = request.json
        password = user_data.get("password")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        user_data["password"] = hashed_password

        user = user_schema.load(user_data)

        user_instance = User(**user)

        db.session.add(user_instance)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/user/update/<int:id>", methods=["PUT"])
def update_user(id):
    try:
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

        response_data = {
            "message": "User updated successfully",
            "user": updated_user_data,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/user/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            abort(404, message="User not found")

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted"}), 200

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/user/login", methods=["POST"])
def login_user():
    try:
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

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/project", methods=["GET"])
@jwt_required
def get_projects():
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        projects = Project.query.paginate(page=page, per_page=per_page)
        project_schema = ProjectSchema(many=True)
        result = project_schema.dump(projects.items)

        return {
            "data": result,
            "page": page,
            "per_page": per_page,
            "total_pages": projects.pages,
            "total_items": projects.total,
        }
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/project/<int:id>", methods=["GET"])
@jwt_required
def get_project(id):
    try:
        project = Project.query.get(id)
        if not project:
            abort(404, message="Project not found")

        project_schema = ProjectSchema()

        result = project_schema.dump(project)
        return result

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/project/create", methods=["POST"])
@projects_router.response(201, ProjectSchema)
@jwt_required
def add_project():
    try:
        project_schema = ProjectSchema()
        project_data = request.json
        project = project_schema.load(project_data)

        project_instance = Project(**project)

        db.session.add(project_instance)
        db.session.commit()

        return jsonify({"message": "Project created successfully"}), 201

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/project/update/<int:id>", methods=["PUT"])
@jwt_required
def update_project(id):
    try:
        project = Project.query.get(id)
        if not project:
            abort(404, message="Project not found")

        project_schema = ProjectSchema()
        updated_data = request.json
        updated_project = project_schema.load(
            updated_data, instance=project, partial=True
        )

        db.session.commit()
        updated_project_data = project_schema.dump(updated_project)

        response_data = {
            "message": "Project updated successfully",
            "project": updated_project_data,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@projects_router.route("/project/delete/<int:id>", methods=["DELETE"])
@jwt_required
def delete_project(id):
    try:
        project = Project.query.get(id)
        if not project:
            abort(404, message="Project not found")

        db.session.delete(project)
        db.session.commit()

        return jsonify({"message": "Project deleted"}), 200

    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500
