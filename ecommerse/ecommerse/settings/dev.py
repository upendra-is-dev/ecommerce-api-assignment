# dev.py

from .base import *  # Import everything from base.py

# Set DEBUG mode based on the environment
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1")

# Allowed Hosts from environment variable (default to localhost)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")

# Example override for SECRET_KEY (can be dev-specific)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-default-key")  # Fallback for dev purposes

# Database setup for development (can be SQLite or other)
DATABASES["default"]["NAME"] = os.getenv("DB_NAME", BASE_DIR / "db.sqlite3")
DATABASES["default"]["USER"] = os.getenv("DB_USER", "user")
DATABASES["default"]["PASSWORD"] = os.getenv("DB_PASSWORD", "password")
DATABASES["default"]["HOST"] = os.getenv("DB_HOST", "localhost")
DATABASES["default"]["PORT"] = os.getenv("DB_PORT", "5432")