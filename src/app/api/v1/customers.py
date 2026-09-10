from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DBSession
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    payload: CustomerCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> Customer:
    customer = Customer(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get("", response_model=list[CustomerResponse])
def list_customers(
    db: DBSession,
    current_user: CurrentUser,
) -> list[Customer]:
    return list(
        db.scalars(
            select(Customer).order_by(Customer.id.desc())
        )
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> Customer:
    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer
