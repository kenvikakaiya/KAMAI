from app import app
from extensions import db
from models import User


with app.app_context():

    admin_email = "admin@kamai.com"

    existing_admin = User.query.filter_by(
        email=admin_email
    ).first()

    if existing_admin:

        existing_admin.role = "admin"

        db.session.commit()

        print("Existing user is now an admin.")

    else:

        admin_user = User(
            username="admin",
            email=admin_email,
            role="admin"
        )

        admin_user.set_password("admin123")

        db.session.add(admin_user)
        db.session.commit()

        print("Admin account created successfully.")

    print()
    print("Admin Email: admin@kamai.com")
    print("Admin Password: admin123")