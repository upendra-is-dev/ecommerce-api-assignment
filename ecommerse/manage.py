#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

def main():
    """Run administrative tasks."""
    
    # Load environment variables from .env or .env.local
    dotenv_path = Path(__file__).resolve().parent/ "ecommerse" / ".env" 
    load_dotenv(dotenv_path=dotenv_path)  # This loads variables from .env
        
    if os.getenv("DJANGO_ENV") == "prod":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerse.settings.prod")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerse.settings.dev")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
