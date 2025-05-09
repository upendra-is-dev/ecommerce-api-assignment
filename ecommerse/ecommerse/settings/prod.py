# prod.py

from .base import *  # Import everything from base.py

# Disable debug in production
DEBUG = False

# Set production-specific allowed hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "yourdomain.com").split(",")

# Retrieve the production secret key
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")  # Should be set in the environment or a secure vault

# Production database setup
DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
DATABASES["default"]["NAME"] = os.getenv("DB_NAME")
DATABASES["default"]["USER"] = os.getenv("DB_USER")
DATABASES["default"]["PASSWORD"] = os.getenv("DB_PASSWORD")
DATABASES["default"]["HOST"] = os.getenv("DB_HOST", "localhost")
DATABASES["default"]["PORT"] = os.getenv("DB_PORT", "5432")
