"""
Seed admin user script with predefined credentials.
Usage: python scripts/seed_admin.py
"""
import os
import sys

# Add the parent directory to Python path so we can import project_flask
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project_flask import create_app
from project_flask.extensions import db
from project_flask.models import User, UserProfile, UserRole, Role
from project_flask.utils.security import hash_password
from dotenv import load_dotenv

load_dotenv()

# Predefined admin credentials
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "AdminPass123!"

def create_admin_user():
    """Create admin user with predefined credentials"""
    app = create_app()
    
    try:
        with app.app_context():
            print("=== Creating Admin User ===")
            
            # Ensure database tables exist
            print("Ensuring database tables exist...")
            db.create_all()
            
            # Ensure roles exist
            print("Checking roles...")
            admin_role = Role.query.filter_by(name="admin").first()
            standard_role = Role.query.filter_by(name="standard").first()
            
            if not admin_role:
                print("Creating 'admin' role...")
                admin_role = Role(name="admin")
                db.session.add(admin_role)
            
            if not standard_role:
                print("Creating 'standard' role...")
                standard_role = Role(name="standard")
                db.session.add(standard_role)
            
            # Commit roles if any were created
            db.session.commit()
            
            # Check if admin user already exists
            existing_user = User.query.filter_by(email=ADMIN_EMAIL.lower()).first()
            if existing_user:
                print(f"✅ Admin user '{ADMIN_EMAIL}' already exists!")
                
                # Check if user has admin role
                has_admin_role = any(role.name == 'admin' for role in existing_user.roles)
                if not has_admin_role:
                    print("Adding admin role to existing user...")
                    user_role = UserRole(user_id=existing_user.id, role_id=admin_role.id)
                    db.session.add(user_role)
                    db.session.commit()
                    print("✅ Admin role added!")
                else:
                    print("User already has admin privileges.")
                return
            
            print(f"Creating admin user: {ADMIN_EMAIL}")
            
            # Create admin user
            admin_user = User(
                email=ADMIN_EMAIL.lower(),
                password_hash=hash_password(ADMIN_PASSWORD),
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
            user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db.session.add(user_role)
            
            # Commit all changes
            db.session.commit()
            
            print(f"✅ Admin user created successfully!")
            print(f"📧 Email: {ADMIN_EMAIL}")
            print(f"🔑 Password: {ADMIN_PASSWORD}")
            print()
            print("🚀 You can now login with these credentials!")
            print("⚠️  Remember to change the password after first login for security.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        try:
            db.session.rollback()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    create_admin_user()
