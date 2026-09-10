from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(min_length=8, max_length=30)


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
