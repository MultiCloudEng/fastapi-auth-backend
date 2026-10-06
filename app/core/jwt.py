from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    to_encode.update({"iat": now, "exp": now + timedelta(minutes=expires_minutes)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and verify a token. Raises jose.JWTError if invalid or expired."""
    # The allowed algorithm is fixed to HS256, so a token cannot choose
    # its own algorithm (e.g. "none").
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
