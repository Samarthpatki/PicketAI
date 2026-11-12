from starlette.status import WS_1005_NO_STATUS_RCVD
from fastapi import HTTPException, status
from pymongo.asynchronous.database import AsyncDatabase

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)

from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserResponse,
    UserRegisterRequest
)

class AuthService:
    def __init__(self, db:AsyncDatabase):
        self.db = db 
        self.collection = self.db["users"]

    
    async def register_user(self, payload: UserRegisterRequest) -> UserResponse :
        """
         1. Checks if email already exists in MongoDB
         2. Hashes password.
         3. Inserts document into 'users' collection
         4. Returns created user representation without password.
        """
        normalized_email = payload.email.strip().lower()
        
        existing_user = await self.collection.find_one({
            "email":normalized_email
            
        })

        if existing_user is not None:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail ="Email already registered"
            )
        user_doc = {
            "email" : normalized_email,
            "hashed_password" : hash_password(payload.password),
            "full_name": payload.full_name
        }

        result = await self.collection.insert_one(user_doc)

        return UserResponse(
            id = str(result.inserted_id),
            full_name= payload.full_name,
            email= payload.email
        )
    
    async def authenticate_user(self, payload: UserLoginRequest) -> TokenResponse:
        """
        1. Finds user by normalized email 
        2. Verifies password hash. 
        3. Generates and returns a JWT access token. 
        """
        normalized_email = payload.email.strip().lower()
        user = await self.collection.find_one({"email" : normalized_email})

        if user is None or not verify_password(
            payload.password, user["hashed_password"]
        ) :
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect email or password",
                headers= {"WWW-Authenticate":"Bearer"},
            )
        access_token = create_access_token(subject=str(user["_id"]))
        return TokenResponse(access_token=access_token,token_type="bearer")

