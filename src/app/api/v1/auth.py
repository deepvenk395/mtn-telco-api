from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DBSession
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest, db: DBSession) -> TokenResponse:
    existing = db.scalar(select(User).where(User.username == payload.username))

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="CUSTOMER",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id), user.role)

    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DBSession) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == payload.username))

    if not user or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(str(user.id), user.role)

    return TokenResponse(access_token=token)


@router.get("/me")
def me(current_user: CurrentUser) -> dict:
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
    }
