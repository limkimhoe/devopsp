from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access: str
    refresh: str

class ProfileOut(BaseModel):
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    timezone: Optional[str] = None
    meta: Optional[dict] = {}

class UserOut(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    is_banned: bool
    roles: List[str]
    profile: Optional[ProfileOut] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class CreateUserRequest(BaseModel):
    email: EmailStr
    temp_password: Optional[str] = None
    roles: Optional[List[str]] = Field(default_factory=list)
    profile: Optional[ProfileOut] = None

class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    timezone: Optional[str] = None
    meta: Optional[dict] = None

class AdminUpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None

class BanRequest(BaseModel):
    reason: Optional[str] = None

class Pagination(BaseModel):
    page: int = 1
    per_page: int = 25

class UsersListOut(BaseModel):
    items: List[UserOut]
    total: int
    page: int
    per_page: int
