from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.db.init_db import init_db


app = FastAPI(
    title="Professional Backend",
    version="1.0"
)

# initialize database
init_db()

# routers
app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "backend running"}