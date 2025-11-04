import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    # App
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///dev.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT / Auth
    # For RS256 provide PRIVATE_KEY / PUBLIC_KEY as PEM strings in .env.
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", None)
    JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY", None)
    JWT_ACCESS_EXPIRES = int(os.getenv("JWT_ACCESS_EXPIRES_SECONDS", 900))  # 15m
    JWT_REFRESH_EXPIRES = int(os.getenv("JWT_REFRESH_EXPIRES_SECONDS", 2592000))  # 30d

    # Refresh token settings
    # If using cookies, configure names and flags
    REFRESH_COOKIE_NAME = os.getenv("REFRESH_COOKIE_NAME", "refresh_token")
    REFRESH_COOKIE_SECURE = os.getenv("REFRESH_COOKIE_SECURE", "false").lower() == "true"
    REFRESH_COOKIE_SAMESITE = os.getenv("REFRESH_COOKIE_SAMESITE", "Lax")

    # Rate limiting
    RATER_LIMIT_DEFAULT = os.getenv("RATER_LIMIT_DEFAULT", "200 per day;50 per hour")

    # Pagination
    DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 25))
    MAX_PER_PAGE = int(os.getenv("MAX_PER_PAGE", 200))

    # Misc
    PREFERRED_URL_SCHEME = "https" if os.getenv("FORCE_HTTPS", "false").lower() == "true" else "http"
