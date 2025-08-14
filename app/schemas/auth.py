# from pydantic import BaseModel, EmailStr
# from typing import Optional

# from datetime import datetime
# # from pydantic import BaseMode


# class UserCreate(BaseModel):
#     """Schema for user registration"""
#     email: EmailStr
#     password: str
#     username: str


# class UserLogin(BaseModel):
#     """Schema for user login"""
#     email: EmailStr
#     password: str


# class Token(BaseModel):
#     """Schema for JWT token response"""
#     access_token: str
#     token_type: str = "bearer"


# class TokenData(BaseModel):
#     """Schema for token payload data"""
#     email: Optional[str] = None
#     user_id: Optional[int] = None


# # class UserResponse(BaseModel):
# #     """Schema for user response (without password)"""
# #     id: int
# #     email: str
# #     username: str
# #     role: str
# #     is_active: bool
# #     created_at: str

# #     class Config:
# #         from_attributes = True 

# class UserResponse(BaseModel):
#     id: int
#     email: str
#     username: str
#     role: str
#     is_active: bool
#     created_at: datetime

#     class Config:
#         orm_mode = True



from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for token payload data"""
    email: Optional[str] = None
    user_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # <-- Updated for Pydantic v2 compatibility
