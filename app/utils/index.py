from jwt import encode, decode, exceptions
import os
from datetime import datetime, timedelta
import bcrypt


def expire_date(days: int) -> datetime:
    current_date = datetime.now()
    new_date = current_date + timedelta(days)
    return new_date


def generate_token(data: dict) -> str:
    token = encode(
        payload={**data, "exp": expire_date(2)},
        key=os.environ.get("SECRET_KEY"),
        algorithm="HS256",
    )
    return token


def validate_token(token: str):
    try:
        decoded_token = decode(
            token,
            key=os.environ.get("SECRET_KEY"),
            algorithms=["HS256"],
        )
        return decoded_token
    except exceptions.DecodeError:
        return None
    except exceptions.ExpiredSignatureError:
        return None


def compare_password(candidate_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        candidate_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
