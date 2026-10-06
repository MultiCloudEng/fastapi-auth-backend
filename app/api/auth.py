from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import DUMMY_PASSWORD_HASH, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email = form_data.username.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    # Always run a bcrypt check, even for unknown emails, so response time
    # does not reveal whether an account exists.
    password_ok = verify_password(
        form_data.password, user.hashed_password if user else DUMMY_PASSWORD_HASH
    )

    # Same error for "no such user" and "wrong password" (no user enumeration).
    if user is None or not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Only reveal the inactive status to someone who knows the password.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token)
