import os

from app.db.session import Base, engine, SessionLocal
from app.models.user import User
from app.core.security import hash_password


def init_db():
    Base.metadata.create_all(bind=engine)

    admin_email = os.getenv("FIRST_ADMIN_EMAIL")
    admin_password = os.getenv("FIRST_ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        return

    db = SessionLocal()

    try:
        email = admin_email.strip().lower()

        user = db.query(User).filter(User.email == email).first()

        if user:
            user.is_admin = True
            user.is_active = True
        else:
            user = User(
                email=email,
                hashed_password=hash_password(admin_password),
                is_active=True,
                is_admin=True
            )
            db.add(user)

        db.commit()

    finally:
        db.close()