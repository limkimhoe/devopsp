from flask import Flask
from dotenv import load_dotenv
import os

from .config import Config
from .extensions import db, migrate, limiter, init_logging
from .blueprints import register_blueprints

load_dotenv()


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    # config
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(Config)

    # init extensions
    init_logging(app)
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # register blueprints (api under /api)
    register_blueprints(app)

    # Database should be initialized manually using: python scripts/init_db.py
    # This prevents Gunicorn worker timeouts on first request

    # routes serving frontend templates
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

    @app.route("/health")
    def health():
        """Simple health check without database operations"""
        return {"status": "ok", "database": "not_tested"}
    
    @app.route("/health/db")
    def health_db():
        """Health check with database connection test"""
        try:
            db.session.execute(db.text("SELECT 1"))
            db_url = app.config['SQLALCHEMY_DATABASE_URI']
            # Show partial URL for security (first 50 chars + indicator)
            url_preview = db_url[:50] + "..." if len(db_url) > 50 else db_url
            using_neondb = 'neondb_owner' in db_url
            return {
                "status": "ok", 
                "database": "connected",
                "url_preview": url_preview,
                "using_neondb": using_neondb
            }
        except Exception as e:
            return {"status": "error", "database": str(e)}, 500

    @app.route("/login.html")
    def login_page():
        from flask import render_template
        return render_template("login.html")

    @app.route("/me.html")
    def me_page():
        from flask import render_template
        return render_template("me.html")

    @app.route("/admin/users.html")
    def admin_users_page():
        from flask import render_template
        return render_template("admin/users.html")

    @app.route("/admin/user-detail.html")
    def admin_user_detail_page():
        from flask import render_template
        return render_template("admin/user-detail.html")

    @app.route("/buildings.html")
    def buildings_page():
        from flask import render_template
        return render_template("buildings.html")

    @app.route("/403.html")
    def forbidden_page():
        from flask import render_template
        return render_template("403.html"), 403

    @app.route("/404.html")
    def notfound_page():
        from flask import render_template
        return render_template("404.html"), 404

    # fallback static file serving for other filenames; do not interfere with /api
    @app.route("/<path:filename>")
    def static_file(filename):
        from flask import abort
        if filename.startswith("api/"):
            abort(404)
        try:
            return app.send_static_file(filename)
        except Exception:
            abort(404)

    return app


# Backwards-compatible entrypoint used by existing Dockerfile
app = create_app()
