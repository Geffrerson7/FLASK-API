from flask import Blueprint, request, jsonify
from app.models.user import User
from app.db import db
import bcrypt


projects_router = Blueprint("projects_router", __name__)

@projects_router.route("/")
def index():
    return "<h1>Hola</h1>"

@projects_router.route("/get-user", methods=['GET'])
def get_users():

    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "password": user.password,
            "date_born": user.date_born,
            "last_session": user.last_session,
            "updated_at": user.updated_at,
            "created_at": user.created_at
        }
        user_list.append(user_data)
    return jsonify(user_list), 200

@projects_router.route("/user", methods=['POST'])
def add_user():
    
    name = request.json["name"]
    email = request.json["email"]
    phone_number = request.json["phone_number"]
    password = request.json["password"]
    date_born = request.json["date_born"]
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name, email, phone_number, hashed_password, date_born)

    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User added successfully"}), 201