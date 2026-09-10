from datetime import datetime

from pydantic import BaseModel, Field


class PlanCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    plan_type: str = Field(min_length=2, max_length=50)
    price_paise: int = Field(gt=0)


class PlanResponse(BaseModel):
    id: int
    name: str
    plan_type: str
    price_paise: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
