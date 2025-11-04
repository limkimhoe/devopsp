import logging
import sys

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def init_logging(app: Flask) -> None:
    """Configure structured JSON logging for the app (simple stdlib JSON)."""
    # Simple JSON-style formatter for logs
    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            data = {
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "funcName": record.funcName,
                "lineno": record.lineno,
            }
            if record.exc_info:
                data["exc_text"] = self.formatException(record.exc_info)
            return str(data)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # Avoid duplicate handlers
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(handler)

    # Example of request logging hook
    @app.before_request
    def log_request_info():
        logging.getLogger("project_flask.request").info(
            "request_start",
            extra={
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
                "user_agent": str(request.user_agent),
            },
        )
