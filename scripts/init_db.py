"""
Init DB helper - creates tables and seeds mandatory roles.

Usage:
  python scripts/init_db.py

This script is intentionally simple for development. For production use Alembic migrations.
"""
import os
from project_flask import create_app
from project_flask.extensions import db
from project_flask.models import Role
from dotenv import load_dotenv

load_dotenv()

app = create_app()
with app.app_context():
    print("Creating database tables (SQLAlchemy create_all)...")
    db.create_all()

    # seed roles
    existing = {r.name for r in Role.query.all()}
    for name in ("admin", "standard"):
        if name not in existing:
            print(f"Inserting role: {name}")
            r = Role(name=name)
            db.session.add(r)
    db.session.commit()
    print("Done.")



# Add to scripts/init_db.py after role seeding
from project_flask.models import User, UserProfile, UserRole
from project_flask.utils.security import hash_password

# Seed admin user
admin_email = "admin@example.com"
admin_password = "AdminPass123!"  # Change this!

existing_admin = User.query.filter_by(email=admin_email).first()
if not existing_admin:
    print(f"Creating admin user: {admin_email}")
    
    # Create user
    admin_user = User(
        email=admin_email,
        password_hash=hash_password(admin_password),
        is_active=True
    )
    db.session.add(admin_user)
    db.session.flush()  # Get the ID
    
    # Create profile
    profile = UserProfile(
        user_id=admin_user.id,
        display_name="System Administrator",
        first_name="Admin",
        last_name="User"
    )
    db.session.add(profile)
    
    # Assign admin role
    admin_role = Role.query.filter_by(name="admin").first()
    if admin_role:
        user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
        db.session.add(user_role)
    
    db.session.commit()
    print(f"Admin user created successfully!")
else:
    print("Admin user already exists")
