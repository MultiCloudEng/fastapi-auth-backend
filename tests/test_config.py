import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _import_config(env):
    return subprocess.run(
        [sys.executable, "-c", "import app.core.config"],
        cwd=ROOT, env=env, capture_output=True, text=True,
    )


def test_missing_secret_key_fails_clearly(tmp_path):
    env = {k: v for k, v in os.environ.items() if k != "SECRET_KEY"}
    env["HOME"] = str(tmp_path)
    r = _import_config(env)
    assert r.returncode != 0
    assert "SECRET_KEY is not set" in r.stderr


def test_short_secret_key_fails(tmp_path):
    env = dict(os.environ, SECRET_KEY="too-short")
    r = _import_config(env)
    assert r.returncode != 0
    assert "at least 32 characters" in r.stderr


def test_postgres_scheme_is_normalized():
    env = dict(os.environ, DATABASE_URL="postgres://u:p@h:5432/db")
    r = subprocess.run(
        [sys.executable, "-c", "from app.core.config import DATABASE_URL; print(DATABASE_URL)"],
        cwd=ROOT, env=env, capture_output=True, text=True,
    )
    assert r.stdout.strip() == "postgresql://u:p@h:5432/db"
