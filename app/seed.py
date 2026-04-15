from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(username="admin").first()

    if not user:
        user = User(username="admin", is_active=True)
        user.set_password("Admin123!")
        db.session.add(user)
        db.session.commit()
        print("User admin created")
    else:
        print("User admin already exists")
