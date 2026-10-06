"""Application settings loaded from environment variables.

Secrets are never hardcoded. The app refuses to start if SECRET_KEY is missing
or too short, so a misconfigured deployment fails loudly instead of running
with a weak or publicly known signing key.
"""
import os

from dotenv import load_dotenv

load_dotenv()  # Loads a local .env file if present; real env vars take precedence.

MIN_SECRET_KEY_LENGTH = 32


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


def _require_secret_key() -> str:
    key = os.getenv("SECRET_KEY", "").strip()
    if not key:
        raise ConfigError(
            "SECRET_KEY is not set. Set it as an environment variable "
            "(see .env.example)."
        )
    if len(key) < MIN_SECRET_KEY_LENGTH:
        raise ConfigError(
            f"SECRET_KEY must be at least {MIN_SECRET_KEY_LENGTH} characters long."
        )
    return key


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip() or "sqlite:///./local.db"
    # Some providers (e.g. older Render/Heroku URLs) use the "postgres://" scheme,
    # which SQLAlchemy 2.x no longer accepts.
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer.") from exc
    if value <= 0:
        raise ConfigError(f"{name} must be positive.")
    return value


SECRET_KEY: str = _require_secret_key()
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = _int_env("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
DATABASE_URL: str = _database_url()

# Brute-force protection for /auth/login (failed attempts per window).
LOGIN_MAX_ATTEMPTS_PER_EMAIL: int = _int_env("LOGIN_MAX_ATTEMPTS_PER_EMAIL", 5)
LOGIN_MAX_ATTEMPTS_PER_IP: int = _int_env("LOGIN_MAX_ATTEMPTS_PER_IP", 20)
LOGIN_WINDOW_SECONDS: int = _int_env("LOGIN_WINDOW_SECONDS", 300)
