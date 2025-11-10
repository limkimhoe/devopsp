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

    # initialize DB and seed roles on first request if needed
    _db_initialized = False
    def _init_db():
        nonlocal _db_initialized
        if _db_initialized:
            return
        try:
            # import models here to avoid circular imports at module import time
            from .models import Role
            # create tables first (safe in most SQLAlchemy backends)
            db.create_all()
            # now check for existing roles after tables are created
            existing = {r.name for r in Role.query.all()}
            for name in ("admin", "standard"):
                if name not in existing:
                    db.session.add(Role(name=name))
            db.session.commit()
            _db_initialized = True
        except Exception as e:
            # avoid crashing the app if DB unavailable; log for diagnosis
            import logging
            logging.getLogger("project_flask.init_db").exception("DB init failed: %s", e)

    @app.before_request
    def ensure_db():
        _init_db()

    # routes serving frontend templates
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

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
