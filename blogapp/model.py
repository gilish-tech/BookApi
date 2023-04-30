from pydantic import BaseModel, validator
from typing import Optional
class SignUpModel(BaseModel):
    username: str
    email:str
    password:str
    @validator('email')
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if len(v) > 12:
            raise ValueError('Password must be less than 12 characters long')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one capital letter')
        return v 


class BookSchema(BaseModel):
    author: str
    title: str
    num_ages: int
    best_seller: bool



class UpdateBookSchema(BaseModel):
    author: Optional[str]
    title:  Optional[str]
    num_ages:  Optional[int]
    best_seller:  Optional[bool]



