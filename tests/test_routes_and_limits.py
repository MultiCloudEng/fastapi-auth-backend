from app.core.security import verify_password
from tests.conftest import login, register


def test_root_is_not_shadowed_by_user_list(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "backend running"


def test_openapi_has_no_duplicate_operations(client):
    spec = client.get("/openapi.json").json()
    ops = [(path, method) for path, methods in spec["paths"].items() for method in methods]
    assert len(ops) == len(set(ops))
    assert "get" in spec["paths"]["/users/"]


def test_legacy_paths_still_work(client):
    assert client.post("/", json={"email": "old@example.com", "password": "old-client-1"}).status_code == 201
    token = login(client, "old@example.com", "old-client-1").json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/me", headers=headers).json()["email"] == "old@example.com"
    assert client.get("/dashboard", headers=headers).status_code == 200


def test_dashboard(client):
    register(client)
    token = login(client).json()["access_token"]
    r = client.get("/users/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json() == {"email": "alice@example.com", "is_active": True, "is_admin": False}


def test_login_is_rate_limited_per_email(client):
    register(client)
    for _ in range(5):
        assert login(client, password="wrong-password").status_code == 401
    blocked = login(client, password="wrong-password")
    assert blocked.status_code == 429
    assert int(blocked.headers["Retry-After"]) > 0
    # Even the correct password is refused while blocked (brute force cannot "win").
    assert login(client).status_code == 429


def test_successful_login_resets_email_counter(client):
    register(client)
    for _ in range(4):
        login(client, password="wrong-password")
    assert login(client).status_code == 200
    for _ in range(4):
        assert login(client, password="wrong-password").status_code == 401


def test_rate_limit_per_ip_across_emails(client):
    for i in range(20):
        login(client, email=f"user{i}@example.com", password="x-wrong-pass")
    assert login(client, email="another@example.com", password="x-wrong-pass").status_code == 429


def test_hash_created_by_old_passlib_version_still_verifies():
    # Generated with passlib's bcrypt handler before the switch to the bcrypt library.
    legacy = "$2b$12$OTEU82uiEZFyDIBvR2SZOe0H89aOj5ZOPjoVrDQqkJOfctdlwdiP."
    assert verify_password("legacy-password-123", legacy)
    assert not verify_password("wrong", legacy)


def test_malformed_hash_does_not_crash():
    assert verify_password("anything", "not-a-bcrypt-hash") is False
