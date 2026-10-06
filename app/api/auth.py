from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import (
    LOGIN_MAX_ATTEMPTS_PER_EMAIL,
    LOGIN_MAX_ATTEMPTS_PER_IP,
    LOGIN_WINDOW_SECONDS,
)
from app.core.jwt import create_access_token
from app.core.rate_limit import LoginRateLimiter
from app.core.security import DUMMY_PASSWORD_HASH, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

login_limiter = LoginRateLimiter(
    max_per_email=LOGIN_MAX_ATTEMPTS_PER_EMAIL,
    max_per_ip=LOGIN_MAX_ATTEMPTS_PER_IP,
    window_seconds=LOGIN_WINDOW_SECONDS,
)


def client_ip(request: Request) -> str:
    # Behind Render's proxy, request.client is the proxy; the original client is
    # the first entry of X-Forwarded-For. A client can fake this header, which only
    # helps against the per-IP limit; the per-email limit still applies.
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={429: {"description": "Too many failed login attempts"}},
)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email = form_data.username.strip().lower()
    ip = client_ip(request)

    wait = login_limiter.retry_after(email, ip)
    if wait:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Try again later.",
            headers={"Retry-After": str(wait)},
        )

    user = db.query(User).filter(User.email == email).first()

    # Always run a bcrypt check, even for unknown emails, so response time
    # does not reveal whether an account exists.
    password_ok = verify_password(
        form_data.password, user.hashed_password if user else DUMMY_PASSWORD_HASH
    )

    # Same error for "no such user" and "wrong password" (no user enumeration).
    if user is None or not password_ok:
        login_limiter.record_failure(email, ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    login_limiter.reset_email(email)

    # Only reveal the inactive status to someone who knows the password.
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    return TokenResponse(access_token=create_access_token(data={"sub": str(user.id)}))
