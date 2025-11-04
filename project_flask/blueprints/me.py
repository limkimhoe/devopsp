from flask import Blueprint, request, jsonify, g
from ..schemas import ProfileOut, UpdateProfileRequest, UserOut
from ..utils.auth import login_required
from ..services.user_service import update_profile
from ..models import User

me_bp = Blueprint("me", __name__, url_prefix="/me")

@me_bp.route("", methods=["GET"])
@login_required
def get_me():
    user: User = g.current_user
    profile = user.profile
    out = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_banned": user.is_banned,
        "roles": [r.name for r in user.roles],
        "profile": {
            "display_name": profile.display_name if profile else None,
            "first_name": profile.first_name if profile else None,
            "last_name": profile.last_name if profile else None,
            "phone": profile.phone if profile else None,
            "avatar_url": profile.avatar_url if profile else None,
            "timezone": profile.timezone if profile else None,
            "meta": profile.meta if profile else {},
        },
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }
    return jsonify(UserOut.model_validate(out).model_dump())

@me_bp.route("", methods=["PATCH"])
@login_required
def patch_me():
    payload = request.get_json() or {}
    try:
        body = UpdateProfileRequest.model_validate(payload)
    except Exception as e:
        return jsonify({"detail": "validation_error", "errors": str(e)}), 422

    user: User = g.current_user
    data = body.model_dump(exclude_none=True)
    profile = update_profile(user, data)
    out = {
        "display_name": profile.display_name,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "phone": profile.phone,
        "avatar_url": profile.avatar_url,
        "timezone": profile.timezone,
        "meta": profile.meta,
    }
    return jsonify(ProfileOut.model_validate(out).model_dump())
