
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


class Config:

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///orderapp.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    UPLOAD_FOLDER = str(
        BASE_DIR / "app" / "static" / "uploads"
    )

    ALLOWED_IMAGE_EXTENSIONS = {
        "png", "jpg", "jpeg", "webp"
    }

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # CSRF protection
    WTF_CSRF_ENABLED = True

    # Payment configuration
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
