from flask import Blueprint, request, jsonify, current_app, make_response, g
from ..schemas import LoginRequest, TokenResponse
from ..models import User
from ..services.auth_service import issue_tokens_for_user, rotate_refresh_token, revoke_refresh_by_token, revoke_all_for_user
from ..services.user_service import get_user_by_id
from ..utils.security import verify_password
from ..extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json() or {}
    try:
        body = LoginRequest.model_validate(payload)
    except Exception as e:
        return jsonify({"detail": "validation_error", "errors": str(e)}), 422

    user = User.query.filter_by(email=body.email.lower().strip()).first()
    if not user:
        return jsonify({"detail": "Invalid credentials"}), 401
    if not verify_password(body.password, user.password_hash):
        return jsonify({"detail": "Invalid credentials"}), 401
    if user.is_banned:
        return jsonify({"detail": "User is banned", "code": "user_banned"}), 403
    if not user.is_active:
        return jsonify({"detail": "User inactive"}), 403

    # record last_login_at
    user.last_login_at = db.func.now()
    db.session.add(user)
    db.session.commit()

    request_meta = {"user_agent": str(request.user_agent), "ip": request.remote_addr}
    tokens = issue_tokens_for_user(user, request_meta=request_meta)
    resp = jsonify(TokenResponse.model_validate(tokens).model_dump())
    # Optionally set refresh cookie if configured
    if current_app.config.get("REFRESH_COOKIE_SECURE", False) or True:
        resp.set_cookie(
            current_app.config.get("REFRESH_COOKIE_NAME", "refresh_token"),
            tokens["refresh"],
            httponly=True,
            secure=current_app.config.get("REFRESH_COOKIE_SECURE", False),
            samesite=current_app.config.get("REFRESH_COOKIE_SAMESITE", "Lax"),
        )
    return resp

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    # refresh token can be in Authorization Bearer or cookie
    token = None
    auth = request.headers.get("Authorization", "")
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get(current_app.config.get("REFRESH_COOKIE_NAME", "refresh_token"))
    if not token:
        return jsonify({"detail": "Missing refresh token"}), 401

    request_meta = {"user_agent": str(request.user_agent), "ip": request.remote_addr}
    try:
        tokens = rotate_refresh_token(token, request_meta=request_meta)
    except ValueError as e:
        # reuse detection or user not allowed
        msg = str(e)
        if msg == "refresh_token_reuse":
            return jsonify({"detail": "Refresh token reuse detected"}), 401
        if msg == "user_not_allowed":
            return jsonify({"detail": "User not allowed"}), 403
        return jsonify({"detail": "Invalid refresh token"}), 401
    resp = jsonify(TokenResponse.model_validate(tokens).model_dump())
    # rotate cookie
    resp.set_cookie(
        current_app.config.get("REFRESH_COOKIE_NAME", "refresh_token"),
        tokens["refresh"],
        httponly=True,
        secure=current_app.config.get("REFRESH_COOKIE_SECURE", False),
        samesite=current_app.config.get("REFRESH_COOKIE_SAMESITE", "Lax"),
    )
    return resp

@auth_bp.route("/logout", methods=["POST"])
def logout():
    token = None
    auth = request.headers.get("Authorization", "")
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get(current_app.config.get("REFRESH_COOKIE_NAME", "refresh_token"))
    if not token:
        return jsonify({"detail": "Missing refresh token"}), 400
    revoke_refresh_by_token(token, reason="logout")
    resp = make_response(jsonify({"detail": "logged_out"}))
    resp.delete_cookie(current_app.config.get("REFRESH_COOKIE_NAME", "refresh_token"))
    return resp

@auth_bp.route("/logout_all", methods=["POST"])
def logout_all():
    # This endpoint requires authentication via access token
    auth_header = request.headers.get("Authorization", "")
    if not (auth_header and auth_header.lower().startswith("bearer ")):
        return jsonify({"detail": "Missing access token"}), 401
    access_token = auth_header.split(" ", 1)[1].strip()
    try:
        import jwt
        alg = current_app.config.get("JWT_ALGORITHM", "RS256")
        if alg.startswith("RS") and current_app.config.get("JWT_PUBLIC_KEY"):
            key = current_app.config["JWT_PUBLIC_KEY"]
        else:
            alg = "HS256"
            key = current_app.config["SECRET_KEY"]
        payload = jwt.decode(access_token, key, algorithms=[alg])
    except Exception:
        return jsonify({"detail": "Invalid access token"}), 401

    if payload.get("type") != "access":
        return jsonify({"detail": "Invalid token type"}), 401
    user_id = payload.get("sub")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404
    revoke_all_for_user(user.id, reason="logout_all")
    resp = make_response(jsonify({"detail": "logged_out_all"}))
    resp.delete_cookie(current_app.config.get("REFRESH_COOKIE_NAME", "refresh_token"))
    return resp
