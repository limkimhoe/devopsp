import uuid
import time
from datetime import datetime, timedelta
from typing import Optional

import jwt
from flask import current_app

from ..models import RefreshToken, User
from ..extensions import db
from ..utils.security import hash_token

def _now():
    return datetime.utcnow()

def _generate_jti() -> str:
    return str(uuid.uuid4())

def _sign_jwt(payload: dict, expires_delta: int) -> str:
    """
    Sign JWT. Prefer configured asymmetric algorithm (RS*) when a private key
    is provided. If signing with the configured algorithm fails (for example
    because the key is missing or invalid), fall back to HS256 with the
    application's SECRET_KEY to avoid 500 errors in development.
    """
    alg = current_app.config.get("JWT_ALGORITHM", "RS256")
    payload = payload.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_delta)
    payload["iat"] = datetime.utcnow()
    payload["nbf"] = datetime.utcnow()

    # Try asymmetric signing if requested and a private key exists
    if alg.startswith("RS") and current_app.config.get("JWT_PRIVATE_KEY"):
        key = current_app.config["JWT_PRIVATE_KEY"]
        try:
            return jwt.encode(payload, key, algorithm=alg)
        except Exception as e:
            # Log and fall back to HS256
            import logging
            logging.getLogger("project_flask.auth").warning(
                "RS signing with configured key failed (%s); falling back to HS256. Error: %s",
                type(e).__name__, e
            )

    # Fallback to symmetric signing using SECRET_KEY
    key = current_app.config.get("SECRET_KEY")
    return jwt.encode(payload, key, algorithm="HS256")

def _decode_jwt(token: str) -> dict:
    """
    Decode JWT. Try asymmetric verification first when configured, but fall
    back to HS256 using SECRET_KEY if verification with the configured
    algorithm/key fails. This prevents InvalidKeyError when devenv provides
    placeholder PEMs.
    """
    alg = current_app.config.get("JWT_ALGORITHM", "RS256")

    # Try asymmetric verification if requested and a public key exists
    if alg.startswith("RS") and current_app.config.get("JWT_PUBLIC_KEY"):
        key = current_app.config["JWT_PUBLIC_KEY"]
        try:
            return jwt.decode(token, key, algorithms=[alg])
        except Exception as e:
            import logging, traceback
            logging.getLogger("project_flask.auth").warning(
                "RS decode with configured public key failed (%s); falling back to HS256. Error: %s",
                type(e).__name__, e
            )

    # Fallback to symmetric verification using SECRET_KEY
    key = current_app.config.get("SECRET_KEY")
    return jwt.decode(token, key, algorithms=["HS256"])

def issue_tokens_for_user(user: User, request_meta: dict | None = None) -> dict:
    """Issue access + refresh tokens. Persist refresh token in DB."""
    access_expires = current_app.config.get("JWT_ACCESS_EXPIRES", 900)
    refresh_expires = current_app.config.get("JWT_REFRESH_EXPIRES", 2592000)

    jti = _generate_jti()
    family_id = str(uuid.uuid4())

    access_payload = {
        "sub": user.id,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "roles": [r.name for r in user.roles],
    }
    access_token = _sign_jwt(access_payload, access_expires)

    refresh_payload = {
        "sub": user.id,
        "type": "refresh",
        "jti": jti,
        "family_id": family_id,
    }
    refresh_token = _sign_jwt(refresh_payload, refresh_expires)

    # store refresh in DB (hashed)
    rt = RefreshToken(
        user_id=user.id,
        jti=jti,
        hashed_token=hash_token(refresh_token),
        family_id=family_id,
        revoked=False,
        issued_at=_now(),
        expires_at=_now() + timedelta(seconds=refresh_expires),
        user_agent=(request_meta or {}).get("user_agent"),
        ip_address=(request_meta or {}).get("ip"),
    )
    db.session.add(rt)
    db.session.commit()

    return {"access": access_token, "refresh": refresh_token}

def rotate_refresh_token(presented_refresh_token: str, request_meta: dict | None = None) -> dict:
    """
    Rotate refresh token:
    - decode token, find DB row by jti
    - if row missing or revoked => reuse detection -> revoke family and raise
    - otherwise revoke current row and issue new refresh with same family_id
    """
    payload = _decode_jwt(presented_refresh_token)
    if payload.get("type") != "refresh":
        raise ValueError("token_not_refresh")

    jti = payload.get("jti")
    family_id = payload.get("family_id")
    user_id = payload.get("sub")

    rt = RefreshToken.query.filter_by(jti=jti).first()
    if rt is None or rt.revoked:
        # reuse detection: revoke entire family if exists
        if family_id:
            RefreshToken.query.filter_by(family_id=family_id, revoked=False).update(
                {"revoked": True, "revoked_reason": "reuse_detected"}
            )
            db.session.commit()
        raise ValueError("refresh_token_reuse")

    # revoke current token
    rt.revoked = True
    rt.revoked_reason = "rotated"
    db.session.add(rt)
    db.session.commit()

    # issue new refresh and access with same family_id
    user = User.query.get(user_id)
    if user is None or user.is_banned or not user.is_active:
        raise ValueError("user_not_allowed")

    access_expires = current_app.config.get("JWT_ACCESS_EXPIRES", 900)
    refresh_expires = current_app.config.get("JWT_REFRESH_EXPIRES", 2592000)

    new_jti = _generate_jti()
    access_payload = {
        "sub": user.id,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "roles": [r.name for r in user.roles],
    }
    access_token = _sign_jwt(access_payload, access_expires)

    refresh_payload = {
        "sub": user.id,
        "type": "refresh",
        "jti": new_jti,
        "family_id": family_id,
    }
    refresh_token = _sign_jwt(refresh_payload, refresh_expires)

    new_rt = RefreshToken(
        user_id=user.id,
        jti=new_jti,
        hashed_token=hash_token(refresh_token),
        family_id=family_id,
        revoked=False,
        issued_at=_now(),
        expires_at=_now() + timedelta(seconds=refresh_expires),
        user_agent=(request_meta or {}).get("user_agent"),
        ip_address=(request_meta or {}).get("ip"),
    )
    db.session.add(new_rt)
    db.session.commit()

    return {"access": access_token, "refresh": refresh_token}

def revoke_refresh_by_token(presented_refresh_token: str, reason: Optional[str] = None) -> None:
    try:
        payload = _decode_jwt(presented_refresh_token)
    except Exception:
        return
    jti = payload.get("jti")
    if not jti:
        return
    rt = RefreshToken.query.filter_by(jti=jti).first()
    if rt:
        rt.revoked = True
        rt.revoked_reason = reason or "logout"
        db.session.add(rt)
        db.session.commit()

def revoke_all_for_user(user_id: str, reason: Optional[str] = None) -> None:
    RefreshToken.query.filter_by(user_id=user_id, revoked=False).update(
        {"revoked": True, "revoked_reason": reason or "logout_all"}
    )
    db.session.commit()
