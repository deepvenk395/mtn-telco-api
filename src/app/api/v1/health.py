from fastapi import APIRouter
from sqlalchemy import text

from app.api.dependencies import DBSession

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready(db: DBSession) -> dict:
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "checks": {
            "database": "ok",
        },
    }
