from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DBSession
from app.models.plan import ServicePlan
from app.schemas.plan import PlanCreate, PlanResponse

router = APIRouter(prefix="/plans", tags=["Service Plans"])


@router.post(
    "",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    payload: PlanCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> ServicePlan:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required",
        )

    plan = ServicePlan(**payload.model_dump())

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


@router.get("", response_model=list[PlanResponse])
def list_plans(
    db: DBSession,
    current_user: CurrentUser,
) -> list[ServicePlan]:
    return list(db.scalars(select(ServicePlan).where(ServicePlan.status == "ACTIVE")))
