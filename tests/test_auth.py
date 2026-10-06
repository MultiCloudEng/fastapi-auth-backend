from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import ALGORITHM, SECRET_KEY
from app.core.jwt import create_access_token
from tests.conftest import deactivate, login, make_admin, register


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_returns_user_without_password(client):
    r = register(client)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "alice@example.com"
    assert body["is_admin"] is False
    assert "password" not in body and "hashed_password" not in body


def test_register_normalizes_email_and_rejects_duplicates(client):
    assert register(client, email="Alice@Example.com").status_code == 201
    assert register(client, email="alice@example.com").status_code == 400


def test_register_rejects_short_password(client):
    assert register(client, password="short").status_code == 422


def test_register_rejects_password_over_72_bytes(client):
    # 40 two-byte characters = 80 bytes, under 72 characters but over 72 bytes.
    assert register(client, password="ä" * 40).status_code == 422


def test_password_is_hashed_in_database(client):
    from app.db.session import SessionLocal
    from app.models.user import User

    register(client)
    db = SessionLocal()
    stored = db.query(User).first().hashed_password
    db.close()
    assert stored != "correct-horse-1"
    assert stored.startswith("$2")  # bcrypt


def test_login_success_returns_bearer_token(client):
    register(client)
    r = login(client)
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"
    payload = jwt.decode(r.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload and "sub" in payload


def test_login_wrong_password_and_unknown_user_give_same_error(client):
    register(client)
    wrong = login(client, password="wrong-password")
    unknown = login(client, email="nobody@example.com")
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_inactive_user_with_wrong_password_is_not_revealed(client):
    register(client)
    deactivate("alice@example.com")
    assert login(client, password="wrong-password").status_code == 401
    assert login(client).status_code == 403


def test_me_requires_token(client):
    assert client.get("/users/me").status_code == 401
    assert client.get("/users/").status_code == 401


def test_me_with_valid_token(client):
    register(client)
    token = login(client).json()["access_token"]
    r = client.get("/users/me", headers=auth_header(token))
    assert r.status_code == 200
    assert r.json()["email"] == "alice@example.com"


def test_expired_token_is_rejected(client):
    register(client)
    token = create_access_token({"sub": "1"}, expires_minutes=-1)
    assert client.get("/users/me", headers=auth_header(token)).status_code == 401


def test_token_signed_with_other_key_is_rejected(client):
    register(client)
    forged = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "CHANGE_ME_SUPER_SECRET_123456789",  # the old hardcoded key
        algorithm="HS256",
    )
    assert client.get("/users/me", headers=auth_header(forged)).status_code == 401


def test_token_with_non_numeric_sub_is_rejected(client):
    token = create_access_token({"sub": "not-a-number"})
    assert client.get("/users/me", headers=auth_header(token)).status_code == 401


def test_list_users_requires_admin(client):
    register(client)
    token = login(client).json()["access_token"]
    assert client.get("/users/", headers=auth_header(token)).status_code == 403

    make_admin("alice@example.com")
    r = client.get("/users/", headers=auth_header(token))
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_inactive_user_token_is_rejected(client):
    register(client)
    token = login(client).json()["access_token"]
    deactivate("alice@example.com")
    assert client.get("/users/me", headers=auth_header(token)).status_code == 403
