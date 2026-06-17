from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.schemas import Token, UserCreate, UserLogin, UserResponse
from src.core.config import settings
from src.core.security import create_access_token
from src.db.database import get_db
from src.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user = register_user(
        db, user_data.username, user_data.email, user_data.password
    )
    return user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(db, user_data.username, user_data.password)
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
