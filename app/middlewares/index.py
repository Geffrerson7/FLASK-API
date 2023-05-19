from functools import wraps
from flask import request, jsonify
from app.utils.index import validate_token

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            response = jsonify({"message": "Token required"})
            response.status_code = 401
            return response
        
        token = token.split(" ")[1]

        validated_token = validate_token(token)
        if not validated_token:
            response = jsonify({"message": "Invalid token"})
            response.status_code = 401
            return response
        
        user_id = validated_token.get('id')
        
        return f(*args, **kwargs)

    return decorated_function