from flask import request, jsonify, redirect, url_for
from flask_smorest import Blueprint, abort
from app.models.user import User
from app.db import db
import bcrypt
from app.schemas import UserSchema


projects_router = Blueprint(
    "projects_router", "projects", url_prefix="/api", description="User API"
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


@projects_router.route("/apidocs")
def api_docs():
    return redirect(url_for("api-docs.openapi_swagger_ui"))
