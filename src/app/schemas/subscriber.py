from datetime import datetime

from pydantic import BaseModel, Field


class SubscriberCreate(BaseModel):
    msisdn: str = Field(min_length=10, max_length=20)
    customer_id: int


class SubscriberResponse(BaseModel):
    id: int
    msisdn: str
    customer_id: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
