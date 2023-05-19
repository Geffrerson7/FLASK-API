from flask import Blueprint, request, jsonify
from app.models.user import User
from app.db import db
import bcrypt
from app.schemas import UserSchema

projects_router = Blueprint("projects_router", __name__)

@projects_router.route("/user", methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify(result), 200

@projects_router.route("/user/<int:id>", methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_schema = UserSchema()
    result = user_schema.dump(user)
    return jsonify(result), 200

@projects_router.route("/user/create", methods=['POST'])
def add_user():
    user_schema = UserSchema()
    user_data = request.json
    password = user_data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_data['password'] = hashed_password

    user = user_schema.load(user_data)

    user_instance = User(**user)

    db.session.add(user_instance)
    db.session.commit()
    
    return jsonify({"message": "User added successfully"}), 201

@projects_router.route("/user/update/<int:id>", methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_schema = UserSchema()
    updated_data = request.json
    updated_user = user_schema.load(updated_data, instance=user, partial=True)
   
    db.session.commit()
    updated_user_data = user_schema.dump(updated_user)

    return jsonify({"message": "User updated successfully", "data":updated_user_data}), 200


@projects_router.route("/user/delete/<int:id>", methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 204

