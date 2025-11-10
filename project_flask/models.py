import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy import func
from .extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    email = db.Column(db.String(320), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_banned = db.Column(db.Boolean, default=False, nullable=False, index=True)
    banned_reason = db.Column(db.Text, nullable=True)
    banned_by = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    banned_at = db.Column(db.DateTime(timezone=True), nullable=True)
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    profile = db.relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    roles = db.relationship("Role", secondary="user_roles", backref="users")

class UserProfile(db.Model):
    __tablename__ = "user_profiles"
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    display_name = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    avatar_url = db.Column(db.Text, nullable=True)
    timezone = db.Column(db.String(64), nullable=True)
    meta = db.Column(JSONB().with_variant(db.JSON, "sqlite"), server_default="{}", nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = db.relationship("User", back_populates="profile")

class UserRole(db.Model):
    __tablename__ = "user_roles"
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = db.Column(db.String(36), db.ForeignKey("roles.id", ondelete="RESTRICT"), primary_key=True)
    assigned_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    jti = db.Column(db.String(128), unique=True, nullable=False)
    hashed_token = db.Column(db.String(256), nullable=True)
    family_id = db.Column(db.String(128), nullable=False, index=True)
    revoked = db.Column(db.Boolean, default=False, nullable=False)
    revoked_reason = db.Column(db.Text, nullable=True)
    issued_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    user_agent = db.Column(db.Text, nullable=True)
    ip_address = db.Column(INET().with_variant(db.String(45), "sqlite"), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(255), nullable=False)
    gml_file_path = db.Column(db.Text, nullable=False)
    texture_file_path = db.Column(db.Text, nullable=False)
    xml_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    actor_user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    target_user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    resource = db.Column(db.String(255), nullable=True)
    method = db.Column(db.String(16), nullable=True)
    details = db.Column(JSONB().with_variant(db.JSON, "sqlite"), server_default="{}", nullable=False)
    ip_address = db.Column(INET().with_variant(db.String(45), "sqlite"), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
