from flask import Blueprint, request, jsonify, g, current_app
from ..schemas import CreateUserRequest, UsersListOut, UserOut, AdminUpdateUserRequest, BanRequest
from ..utils.auth import login_required, require_role
from ..services.user_service import create_user, list_users, get_user_by_id, update_user_admin, ban_user, unban_user
from ..services.auth_service import revoke_all_for_user
from ..models import User
from ..extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin/users")

@admin_bp.route("", methods=["POST"])
@login_required
@require_role("admin")
def create_user_endpoint():
    payload = request.get_json() or {}
    try:
        body = CreateUserRequest.model_validate(payload)
    except Exception as e:
        return jsonify({"detail": "validation_error", "errors": str(e)}), 422

    # temp_password required by service; generate if missing
    temp_password = body.temp_password or "ChangeMe123!"
    roles = body.roles or []
    profile = body.profile.model_dump() if body.profile else None

    user = create_user(body.email, temp_password, roles, profile)
    out = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_banned": user.is_banned,
        "roles": [r.name for r in user.roles],
        "profile": profile or {},
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }
    return jsonify(UserOut.model_validate(out).model_dump()), 201

@admin_bp.route("", methods=["GET"])
@login_required
@require_role("admin")
def list_users_endpoint():
    # query params: page, per_page, search, role, is_banned, is_active, sort
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", current_app.config.get("DEFAULT_PER_PAGE", 25)))
    per_page = min(per_page, current_app.config.get("MAX_PER_PAGE", 200))
    search = request.args.get("search")
    role = request.args.get("role")
    is_banned = request.args.get("is_banned")
    is_active = request.args.get("is_active")
    sort = request.args.get("sort", "created_at_desc")

    if is_banned is not None:
        is_banned = is_banned.lower() in ("1", "true", "yes")
    if is_active is not None:
        is_active = is_active.lower() in ("1", "true", "yes")

    items, total = list_users(page=page, per_page=per_page, search=search, role=role, is_banned=is_banned, is_active=is_active, sort=sort)
    out_items = []
    for user in items:
        profile = user.profile
        out_items.append({
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_banned": user.is_banned,
            "roles": [r.name for r in user.roles],
            "profile": {
                "display_name": profile.display_name if profile else None
            } if profile else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        })
    # compute total pages for frontend pagination helpers
    total_pages = (total + per_page - 1) // per_page if per_page else 0
    resp = {
        "items": out_items,
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "per_page": per_page,
    }
    # keep the UsersListOut schema for validation (it ignores extra fields)
    return jsonify(UsersListOut.model_validate(resp).model_dump()), 200

@admin_bp.route("/<user_id>", methods=["GET"])
@login_required
@require_role("admin")
def get_user_endpoint(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404
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
        } if profile else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }
    return jsonify(UserOut.model_validate(out).model_dump())

@admin_bp.route("/<user_id>", methods=["PATCH"])
@login_required
@require_role("admin")
def patch_user_endpoint(user_id):
    payload = request.get_json() or {}
    try:
        body = AdminUpdateUserRequest.model_validate(payload)
    except Exception as e:
        return jsonify({"detail": "validation_error", "errors": str(e)}), 422

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404

    user = update_user_admin(user, email=body.email, roles=body.roles, is_active=body.is_active)
    out = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_banned": user.is_banned,
        "roles": [r.name for r in user.roles],
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }
    return jsonify(UserOut.model_validate(out).model_dump())

@admin_bp.route("/<user_id>/ban", methods=["POST"])
@login_required
@require_role("admin")
def ban_user_endpoint(user_id):
    payload = request.get_json() or {}
    try:
        body = BanRequest.model_validate(payload)
    except Exception as e:
        return jsonify({"detail": "validation_error", "errors": str(e)}), 422

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404
    actor = getattr(g, "current_user", None)
    user = ban_user(actor.id if actor else None, user, reason=body.reason)
    # revoke all refresh tokens when banned
    revoke_all_for_user(user.id, reason="banned")
    return jsonify({"detail": "user_banned", "user_id": user.id}), 200

@admin_bp.route("/<user_id>/unban", methods=["POST"])
@login_required
@require_role("admin")
def unban_user_endpoint(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404
    user = unban_user(user)
    return jsonify({"detail": "user_unbanned", "user_id": user.id}), 200
