import os
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, redirect, g

SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))


def generate_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": username,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("auth_token")
        if not token:
            return redirect("/login")

        payload = verify_token(token)
        if not payload:
            return redirect("/login")

        g.user = payload
        return view_func(*args, **kwargs)

    return wrapper
