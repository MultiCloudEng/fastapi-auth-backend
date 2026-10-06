from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import DashboardResponse, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Old paths from the first version of the API, kept so existing clients keep
# working. They are marked deprecated in the docs; use the /users/... paths.
legacy_router = APIRouter(tags=["Deprecated"], deprecated=True)


def register(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        is_active=True,
        is_admin=False,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db.refresh(db_user)
    return db_user


def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


def dashboard(current_user: User = Depends(get_current_user)) -> DashboardResponse:
    return DashboardResponse(
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
    )


def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> list[User]:
    return db.query(User).order_by(User.id).all()


created = {"response_model": UserResponse, "status_code": status.HTTP_201_CREATED}

router.add_api_route("/", register, methods=["POST"], summary="Register", **created)
router.add_api_route("/", list_users, methods=["GET"], response_model=list[UserResponse],
                     summary="List users (admin only)")
router.add_api_route("/me", read_me, methods=["GET"], response_model=UserResponse,
                     summary="Current user")
router.add_api_route("/dashboard", dashboard, methods=["GET"], response_model=DashboardResponse,
                     summary="Current user summary")

legacy_router.add_api_route("/", register, methods=["POST"], summary="Register (use POST /users/)", **created)
legacy_router.add_api_route("/me", read_me, methods=["GET"], response_model=UserResponse,
                            summary="Current user (use GET /users/me)")
legacy_router.add_api_route("/dashboard", dashboard, methods=["GET"], response_model=DashboardResponse,
                            summary="Current user summary (use GET /users/dashboard)")
