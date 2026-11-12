from typing import Annotated

from fastapi import APIRouter, Depends,status
from pymongo.asynchronous.database  import AsyncDatabase

from app.core.config import settings
from app.db.session import db_manager
from app.schemas.auth import (
    TokenResponse,
        UserLoginRequest,
        UserRegisterRequest,
        UserResponse
)
from app.services.auth_services import AuthService

router = APIRouter(prefix="/auth",tags=["Authentication"])
settings = settings()

def get_auth_service() -> AuthService:
    db: AsyncDatabase = db_manager.get_database(settings.DATABASE_NAME)
    return AuthService(db)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code= status.HTTP_201_CREATED
)
async def register(
    payload: UserRegisterRequest,
    auth_service: Annotated[AuthService,Depends(get_auth_service)],
) -> UserResponse :
    return await auth_service.register_user(payload)

@router.post(
    "login",
    response_model=TokenResponse,
    status_code= status.HTTP_200_OK
)
async def login(
    payload:UserLoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenResponse : 
    return await auth_service.authencticate_user(payload)



