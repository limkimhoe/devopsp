"""
Init DB helper - creates tables and seeds mandatory roles and admin user.

Usage:
  python scripts/init_db.py

This script is intentionally simple for development. For production use Alembic migrations.
"""
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to Python path so we can import project_flask
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# DOCKER FIX: Clear Docker environment variables before loading .env
docker_vars_to_clear = [
    'DATABASE_URL', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 
    'POSTGRES_DB', 'POSTGRES_HOST', 'POSTGRES_PORT'
]

print("🔧 Clearing Docker environment variables...")
for var in docker_vars_to_clear:
    if var in os.environ:
        del os.environ[var]
        print(f"   Cleared: {var}")

# Load .env file
print("📁 Loading .env file...")
load_dotenv(override=True)

# Verify DATABASE_URL from .env
db_url = os.getenv('DATABASE_URL', 'NOT FOUND')
if 'neondb_owner' in db_url:
    print("✅ Using NeonDB connection")
else:
    print(f"⚠️  Warning: DATABASE_URL may not be pointing to NeonDB: {db_url[:50]}...")

from project_flask import create_app
from project_flask.extensions import db
from project_flask.models import Role, User, UserProfile, UserRole
from project_flask.utils.security import hash_password

def init_database():
    """Initialize database with tables, roles, and admin user"""
    app = create_app()
    
    try:
        with app.app_context():
            print("=== Database Initialization ===")
            
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Seed roles
            print("Seeding roles...")
            existing = {r.name for r in Role.query.all()}
            for name in ("admin", "standard"):
                if name not in existing:
                    print(f"  Creating role: {name}")
                    r = Role(name=name)
                    db.session.add(r)
                else:
                    print(f"  Role '{name}' already exists")
            
            db.session.commit()
            print("✅ Roles seeded successfully")
            
            # Seed admin user
            print("Seeding admin user...")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "AdminPass123!")
            
            existing_admin = User.query.filter_by(email=admin_email.lower()).first()
            if not existing_admin:
                print(f"  Creating admin user: {admin_email}")
                
                # Create user
                admin_user = User(
                    email=admin_email.lower(),
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
                print(f"✅ Admin user created successfully!")
                print(f"📧 Email: {admin_email}")
                print(f"🔑 Password: {admin_password}")
            else:
                print(f"  Admin user '{admin_email}' already exists")
                
                # Check if user has admin role
                has_admin_role = any(role.name == 'admin' for role in existing_admin.roles)
                if not has_admin_role:
                    print("  Adding admin role to existing user...")
                    admin_role = Role.query.filter_by(name="admin").first()
                    if admin_role:
                        user_role = UserRole(user_id=existing_admin.id, role_id=admin_role.id)
                        db.session.add(user_role)
                        db.session.commit()
                        print("  ✅ Admin role added!")
                else:
                    print("  User already has admin privileges")
            
            print("✅ Database initialization completed successfully!")
            print()
            print("🚀 Your database is ready!")
            print("⚠️  Remember to change the admin password after first login for security.")
            
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    init_database()
