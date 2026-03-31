from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
def health_check():
    return {"status": "ok"}

from typing import Generator

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()