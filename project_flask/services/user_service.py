from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy import or_, func

from ..models import User, UserProfile, Role, UserRole
from ..extensions import db
from ..utils.security import hash_password

def create_user(email: str, temp_password: str, roles: List[str], profile_data: Optional[dict] = None) -> User:
    password_hash = hash_password(temp_password or "ChangeMe123!")
    user = User(email=email.lower().strip(), password_hash=password_hash)
    db.session.add(user)
    db.session.flush()  # assign id

    # profile
    if profile_data:
        profile = UserProfile(user_id=user.id, **profile_data)
        db.session.add(profile)

    # roles
    if roles:
        role_objs = Role.query.filter(Role.name.in_(roles)).all()
        for r in role_objs:
            ur = UserRole(user_id=user.id, role_id=r.id)
            db.session.add(ur)

    db.session.commit()
    return user

def get_user_by_id(user_id: str) -> Optional[User]:
    return User.query.get(user_id)

def update_user_admin(user: User, email: Optional[str] = None, roles: Optional[List[str]] = None, is_active: Optional[bool] = None) -> User:
    if email:
        user.email = email.lower().strip()
    if is_active is not None:
        user.is_active = is_active
    if roles is not None:
        # replace roles
        # remove existing
        db.session.query(UserRole).filter_by(user_id=user.id).delete()
        if roles:
            role_objs = Role.query.filter(Role.name.in_(roles)).all()
            for r in role_objs:
                ur = UserRole(user_id=user.id, role_id=r.id)
                db.session.add(ur)
    db.session.add(user)
    db.session.commit()
    return user

def update_profile(user: User, data: dict) -> UserProfile:
    profile = user.profile
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.session.add(profile)
    for k, v in data.items():
        if hasattr(profile, k) and v is not None:
            setattr(profile, k, v)
    db.session.commit()
    return profile

def list_users(page: int = 1, per_page: int = 25, search: Optional[str] = None, role: Optional[str] = None,
               is_banned: Optional[bool] = None, is_active: Optional[bool] = None, sort: str = "created_at_desc") -> Tuple[List[User], int]:
    q = User.query

    if search:
        s = f"%{search.lower()}%"
        q = q.join(UserProfile, isouter=True).filter(
            or_(func.lower(User.email).like(s),
                func.lower(UserProfile.display_name).like(s),
                func.lower(UserProfile.first_name).like(s),
                func.lower(UserProfile.last_name).like(s))
        )

    if role:
        q = q.join(UserRole).join(Role).filter(Role.name == role)

    if is_banned is not None:
        q = q.filter(User.is_banned == is_banned)

    if is_active is not None:
        q = q.filter(User.is_active == is_active)

    if sort == "created_at_asc":
        q = q.order_by(User.created_at.asc(), User.id.asc())
    else:
        q = q.order_by(User.created_at.desc(), User.id.desc())

    # remove ordering before counting to avoid GROUP BY errors with joins
    total = q.order_by(None).with_entities(func.count(User.id)).scalar() or 0
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    return items, total

def ban_user(actor_user_id: Optional[str], user: User, reason: Optional[str] = None) -> User:
    user.is_banned = True
    user.banned_reason = reason
    user.banned_by = actor_user_id
    user.banned_at = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    return user

def unban_user(user: User) -> User:
    user.is_banned = False
    user.banned_reason = None
    user.banned_by = None
    user.banned_at = None
    db.session.add(user)
    db.session.commit()
    return user
