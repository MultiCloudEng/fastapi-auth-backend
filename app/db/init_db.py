import logging
import os

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.user import User

logger = logging.getLogger(__name__)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    admin_email = os.getenv("FIRST_ADMIN_EMAIL", "").strip().lower()
    admin_password = os.getenv("FIRST_ADMIN_PASSWORD", "")

    if not admin_email or not admin_password:
        return

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == admin_email).first()

        if existing is None:
            db.add(
                User(
                    email=admin_email,
                    hashed_password=hash_password(admin_password),
                    is_active=True,
                    is_admin=True,
                )
            )
            db.commit()
            logger.info("Created first admin account.")
        elif not existing.is_admin:
            # Security: never promote an existing account automatically.
            # Registration is public, so someone could register the admin email
            # first and would otherwise be made admin on the next restart.
            logger.warning(
                "FIRST_ADMIN_EMAIL belongs to an existing non-admin account; "
                "not promoting it automatically."
            )
    finally:
        db.close()
