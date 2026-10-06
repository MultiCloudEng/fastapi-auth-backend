from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.users import legacy_router, router as users_router
from app.db.init_db import init_db

app = FastAPI(
    title="FastAPI Auth Backend",
    version="1.1",
    description="Registration and login with bcrypt, JWT access tokens and admin-only endpoints.",
)

init_db()


@app.get("/", tags=["Health"], summary="Service info")
def root():
    return {"status": "backend running", "docs": "/docs"}


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(legacy_router)
