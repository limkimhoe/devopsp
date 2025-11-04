from functools import wraps
from typing import Optional, Callable
import jwt
from flask import request, current_app, jsonify, g

from ..models import User
from ..extensions import db

def _decode_access_token(token: str) -> dict:
    """
    Decode access token. Try configured asymmetric verification first when a
    public key is provided; if verification fails, fall back to HS256 using
    the application's SECRET_KEY. This mirrors the behavior in auth_service.
    """
    alg = current_app.config.get("JWT_ALGORITHM", "RS256")

    # Try asymmetric verification if requested and a public key exists
    if alg.startswith("RS") and current_app.config.get("JWT_PUBLIC_KEY"):
        key = current_app.config["JWT_PUBLIC_KEY"]
        try:
            return jwt.decode(token, key, algorithms=[alg])
        except Exception:
            # fall back to HS256
            pass

    # Fallback to symmetric verification using SECRET_KEY
    key = current_app.config.get("SECRET_KEY")
    return jwt.decode(token, key, algorithms=["HS256"])

def get_bearer_token() -> Optional[str]:
    auth = request.headers.get("Authorization", "")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    # fallback to access_token param
    return request.args.get("access_token")

def login_required(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return jsonify({"detail": "Missing auth token"}), 401
        try:
            payload = _decode_access_token(token)
        except Exception:
            return jsonify({"detail": "Invalid token"}), 401
        if payload.get("type") != "access":
            return jsonify({"detail": "Token not access"}), 401
        user_id = payload.get("sub")
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"detail": "User not found"}), 401
        if user.is_banned:
            return jsonify({"detail": "User is banned", "code": "user_banned"}), 403
        if not user.is_active:
            return jsonify({"detail": "User inactive"}), 403
        # attach user and token payload to flask.g
        g.current_user = user
        g.token_payload = payload
        return fn(*args, **kwargs)
    return wrapper

def require_role(role_name: str):
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # ensure logged in
            if not hasattr(g, "current_user"):
                # try to enforce login_required
                return login_required(lambda *a, **k: fn(*a, **k))(*args, **kwargs)
            user: User = g.current_user
            role_names = {r.name for r in user.roles}
            if role_name not in role_names:
                return jsonify({"detail": "Insufficient privileges"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
