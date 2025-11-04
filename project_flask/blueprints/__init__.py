from flask import Blueprint
from typing import List
from .auth import auth_bp
from .me import me_bp
from .admin_users import admin_bp

def register_blueprints(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")
    # register sub-blueprints under /api
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(me_bp)
    api_bp.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
