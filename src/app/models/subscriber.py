from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(primary_key=True)
    msisdn: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="ACTIVE",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
