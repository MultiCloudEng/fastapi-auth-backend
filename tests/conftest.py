import os
import tempfile

import pytest

# Configure the app BEFORE importing it: settings are read at import time.
_db_dir = tempfile.mkdtemp()
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-123456"
os.environ["DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ.pop("FIRST_ADMIN_EMAIL", None)
os.environ.pop("FIRST_ADMIN_PASSWORD", None)

from fastapi.testclient import TestClient  # noqa: E402

from app.db.session import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402


@pytest.fixture(autouse=True)
def clean_db():
    from app.api.auth import login_limiter

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    login_limiter.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


def register(client, email="alice@example.com", password="correct-horse-1"):
    return client.post("/users/", json={"email": email, "password": password})


def login(client, email="alice@example.com", password="correct-horse-1"):
    return client.post("/auth/login", data={"username": email, "password": password})


def make_admin(email):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        user.is_admin = True
        db.commit()
    finally:
        db.close()


def deactivate(email):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        user.is_active = False
        db.commit()
    finally:
        db.close()
