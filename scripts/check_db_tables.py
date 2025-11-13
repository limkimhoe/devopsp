"""
Check what tables exist in the database and their contents.
"""
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to Python path so we can import project_flask
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project_flask import create_app
from project_flask.extensions import db
from project_flask.models import Role, User, UserProfile, UserRole

load_dotenv()

def check_database():
    """Check database tables and their contents"""
    app = create_app()
    
    try:
        with app.app_context():
            print("=== Database Tables Check ===")
            
            # Check if we can connect
            try:
                db.session.execute(db.text("SELECT 1"))
                print("✅ Database connection successful")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                return
            
            # Get all table names
            try:
                result = db.session.execute(db.text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """))
                tables = [row[0] for row in result.fetchall()]
                print(f"\n📋 Tables in database: {tables}")
                
                if not tables:
                    print("⚠️  No tables found in database!")
                    return
                    
            except Exception as e:
                print(f"❌ Error fetching table names: {e}")
                return
            
            # Check each model table
            models_to_check = [
                ("roles", Role),
                ("users", User), 
                ("user_profiles", UserProfile),
                ("user_roles", UserRole)
            ]
            
            for table_name, model_class in models_to_check:
                try:
                    count = db.session.query(model_class).count()
                    print(f"📊 {table_name}: {count} records")
                    
                    if table_name == "roles":
                        roles = db.session.query(Role).all()
                        for role in roles:
                            print(f"  - Role: {role.name} (ID: {role.id})")
                    
                    if table_name == "users":
                        users = db.session.query(User).all()
                        for user in users:
                            print(f"  - User: {user.email} (ID: {user.id}, Active: {user.is_active})")
                            
                except Exception as e:
                    print(f"❌ Error checking {table_name}: {e}")
            
            # Try to manually create tables if they don't exist
            print("\n🔧 Attempting to create tables...")
            db.create_all()
            print("✅ create_all() completed")
            
            # Check again after create_all
            result = db.session.execute(db.text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables_after = [row[0] for row in result.fetchall()]
            print(f"📋 Tables after create_all(): {tables_after}")
            
    except Exception as e:
        print(f"❌ Error during database check: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
