from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DBSession
from app.models.customer import Customer
from app.models.subscriber import Subscriber
from app.schemas.subscriber import (
    SubscriberCreate,
    SubscriberResponse,
)

router = APIRouter(prefix="/subscribers", tags=["Subscribers"])


@router.post(
    "",
    response_model=SubscriberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subscriber(
    payload: SubscriberCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> Subscriber:
    customer = db.get(Customer, payload.customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    existing = db.scalar(
        select(Subscriber).where(
            Subscriber.msisdn == payload.msisdn
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MSISDN already exists",
        )

    subscriber = Subscriber(
        msisdn=payload.msisdn,
        customer_id=payload.customer_id,
    )

    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)

    return subscriber


@router.get(
    "/{subscriber_id}",
    response_model=SubscriberResponse,
)
def get_subscriber(
    subscriber_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> Subscriber:
    subscriber = db.get(Subscriber, subscriber_id)

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found",
        )

    return subscriber
