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
