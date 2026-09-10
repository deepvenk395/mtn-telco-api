from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ServicePlan(Base):
    __tablename__ = "service_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )
    plan_type: Mapped[str] = mapped_column(String(50))
    price_paise: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(30),
        default="ACTIVE",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
