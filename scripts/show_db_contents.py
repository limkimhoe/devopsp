"""
Show detailed contents of all database tables.
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

def show_database_contents():
    """Show detailed contents of all database tables"""
    app = create_app()
    
    try:
        with app.app_context():
            print("=== COMPLETE DATABASE CONTENTS ===\n")
            
            # Show Roles
            print("🔐 ROLES TABLE:")
            roles = db.session.query(Role).all()
            for role in roles:
                print(f"  ID: {role.id}")
                print(f"  Name: {role.name}")
                print(f"  Created: {role.created_at}")
                print()
            
            # Show Users
            print("👤 USERS TABLE:")
            users = db.session.query(User).all()
            for user in users:
                print(f"  ID: {user.id}")
                print(f"  Email: {user.email}")
                print(f"  Active: {user.is_active}")
                print(f"  Has Password: {'Yes' if user.password_hash else 'No'}")
                print(f"  Created: {user.created_at}")
                print(f"  Updated: {user.updated_at}")
                print()
            
            # Show User Profiles
            print("📋 USER PROFILES TABLE:")
            profiles = db.session.query(UserProfile).all()
            for profile in profiles:
                user = db.session.query(User).filter_by(id=profile.user_id).first()
                print(f"  User ID: {profile.user_id}")
                print(f"  User: {user.email if user else 'Unknown'}")
                print(f"  Display Name: {profile.display_name}")
                print(f"  First Name: {profile.first_name}")
                print(f"  Last Name: {profile.last_name}")
                print(f"  Updated: {profile.updated_at}")
                print()
            
            # Show User Roles
            print("🎭 USER ROLES TABLE:")
            user_roles = db.session.query(UserRole).all()
            for user_role in user_roles:
                user = db.session.query(User).filter_by(id=user_role.user_id).first()
                role = db.session.query(Role).filter_by(id=user_role.role_id).first()
                print(f"  User: {user.email if user else 'Unknown'} ({user_role.user_id})")
                print(f"  Role: {role.name if role else 'Unknown'} ({user_role.role_id})")
                print(f"  Assigned: {user_role.assigned_at}")
                print()
            
            # Summary
            print("📊 SUMMARY:")
            print(f"  Roles: {len(roles)}")
            print(f"  Users: {len(users)}")
            print(f"  User Profiles: {len(profiles)}")
            print(f"  User Role Assignments: {len(user_roles)}")
            
            # Check admin user specifically
            print("\n🔍 ADMIN USER CHECK:")
            admin_user = db.session.query(User).filter_by(email="admin@example.com").first()
            if admin_user:
                print(f"  ✅ Admin user exists: {admin_user.email}")
                print(f"  ✅ User is active: {admin_user.is_active}")
                
                admin_roles = db.session.query(UserRole).filter_by(user_id=admin_user.id).all()
                print(f"  ✅ Role assignments: {len(admin_roles)}")
                for ur in admin_roles:
                    role = db.session.query(Role).filter_by(id=ur.role_id).first()
                    print(f"    - {role.name if role else 'Unknown'}")
            else:
                print("  ❌ Admin user not found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_database_contents()
