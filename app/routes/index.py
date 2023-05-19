from flask import Blueprint, request, jsonify
from app.models.user import User
from app.db import db
import bcrypt
from app.schemas import UserSchema

projects_router = Blueprint("projects_router", __name__)

@projects_router.route("/get-user", methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify(result), 200

import bcrypt

@projects_router.route("/user", methods=['POST'])
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

