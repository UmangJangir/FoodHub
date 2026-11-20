
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Database
db = SQLAlchemy()

# User authentication
login_manager = LoginManager()

# Database migrations
migrate = Migrate()

# CSRF protection
csrf = CSRFProtect()
