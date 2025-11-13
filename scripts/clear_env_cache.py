#!/usr/bin/env python3
"""
Clear environment variable cache and reload .env file.
Use this script if you modify .env and need to clear Python's environment cache.
"""
import os
from dotenv import load_dotenv

def clear_and_reload_env():
    """Clear environment cache and reload .env file"""
    print("🔄 Clearing environment variable cache...")
    
    # Clear specific environment variables that might be cached
    env_vars_to_clear = [
        'DATABASE_URL',
        'FLASK_ENV',
        'SECRET_KEY',
        'ADMIN_EMAIL',
        'ADMIN_PASSWORD'
    ]
    
    for var in env_vars_to_clear:
        if var in os.environ:
            del os.environ[var]
            print(f"   Cleared: {var}")
    
    print("📁 Reloading .env file...")
    load_dotenv(override=True)
    
    print("✅ Environment cache cleared and .env reloaded!")
    
    # Verify key variables
    print("\n🔍 Verification:")
    db_url = os.getenv('DATABASE_URL', 'NOT FOUND')
    if db_url != 'NOT FOUND':
        print(f"   DATABASE_URL: {db_url[:50]}...")
        print(f"   Using NeonDB: {'neondb_owner' in db_url}")
    else:
        print("   DATABASE_URL: NOT FOUND")
    
    flask_env = os.getenv('FLASK_ENV', 'NOT FOUND')
    print(f"   FLASK_ENV: {flask_env}")

if __name__ == "__main__":
    clear_and_reload_env()
