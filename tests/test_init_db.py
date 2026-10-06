from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.user import User
from tests.conftest import register


def _get(email):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()


def test_first_admin_created(monkeypatch):
    monkeypatch.setenv("FIRST_ADMIN_EMAIL", "Admin@Example.com")
    monkeypatch.setenv("FIRST_ADMIN_PASSWORD", "a-strong-admin-password")
    init_db()
    assert _get("admin@example.com").is_admin is True


def test_existing_user_is_not_promoted(client, monkeypatch):
    register(client, email="admin@example.com")  # attacker registers the admin email first
    monkeypatch.setenv("FIRST_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("FIRST_ADMIN_PASSWORD", "a-strong-admin-password")
    init_db()
    assert _get("admin@example.com").is_admin is False
