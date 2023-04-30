from passlib.context import CryptContext
from fastapi import HTTPException,status, Depends
from pydantic import ValidationError
# from app.schemas import TokenPayload, SystemUser
# im
from .database import get_db
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USER_COLLECTION_NAME = "Users"
BOOK_COLLECTION_NAME = "Books"

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)





ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ["JWT_SECRET_KEY"]    # should be kept secret




def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt




async def get_current_user(token: str = Depends(reuseable_oauth)) :
    # print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
    database =  get_db()
    db =  database[USER_COLLECTION_NAME]

    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = payload
        print(type(token_data))
        print( token_data)
        
        if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # print(token_data["sub"] )   
    
    return token_data["sub"]