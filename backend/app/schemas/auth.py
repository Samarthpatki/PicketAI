from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(...,min_length=4, description="Password must be atleast 4 characters" )
    full_name: str | None = None


class UserLoginRequest(BaseModel):
    email : EmailStr
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"


class UserResponse(BaseModel):
    id:str
    email:EmailStr
    full_name :str |None = None


