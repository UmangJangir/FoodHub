
from getpass import getpass

from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    print("\n========== FOODHUB ADMIN SETUP ==========\n")

    email = input("Admin email: ").strip().lower()

    if not email:
        print("Email cannot be empty.")
        raise SystemExit

    user = User.query.filter_by(email=email).first()

    if user:
        print(f"\nAccount found: {user.full_name} ({user.email})")
        confirm = input("Make this account an admin? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Operation cancelled.")
            raise SystemExit

        user.role = "admin"
        db.session.commit()
        print("\nExisting account is now an admin!")

    else:
        full_name = input("Admin full name: ").strip()
        phone = input("Phone number (optional): ").strip() or None

        if not full_name:
            print("Name cannot be empty.")
            raise SystemExit

        password = getpass("Create admin password: ")
        confirm_password = getpass("Confirm admin password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            raise SystemExit

        if password != confirm_password:
            print("Passwords do not match.")
            raise SystemExit

        admin = User(
            full_name=full_name,
            email=email,
            phone=phone,
            role="admin"
        )

        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        print("\nAdmin account created successfully!")

    print("\nAdmin login URL: /login")
    print("Admin dashboard URL: /admin")
    print("\n========================================\n")
