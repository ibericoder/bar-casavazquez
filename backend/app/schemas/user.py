from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from ..models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.STAFF
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

class UserInDB(User):
    hashed_password: str

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str