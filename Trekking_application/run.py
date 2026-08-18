from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            first_name="Govinda",
            last_name="Pathak",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),
            phone="9876543210",
            role="admin",
            is_approved=True
        )
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)