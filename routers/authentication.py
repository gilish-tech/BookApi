from fastapi import APIRouter

from fastapi import FastAPI,status, HTTPException,Depends
from fastapi.security  import OAuth2PasswordRequestForm
from settings.database import get_db
from blogapp.model import SignUpModel
from settings.settings import USER_COLLECTION_NAME, get_current_user, get_hashed_password,verify_password, create_access_token, create_refresh_token





router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
async def login_user(request:OAuth2PasswordRequestForm =  Depends()):
        db =  get_db()  
        users_col = db[USER_COLLECTION_NAME]
        email =  request.username  #Note i used request.username because that is what Oauth... use by default
        print(email)
        user = users_col.find_one({"email":email})
        if user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        hashed_pass = user['password']
        if not verify_password(request.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or ppppp  password"
            )
        subject = {"id": str(user["_id"]) ,"email":str(user["email"])}
        print("subject is ",subject)
        return {
            "access_token": create_access_token(subject),
            "refresh_token": create_refresh_token(subject),
        }



@router.post("/signup")
def signup_users(request:SignUpModel):
    db =  get_db()  
    users_col = db[USER_COLLECTION_NAME]
    user = users_col.find_one({"email":request.email})
    if user is not None :
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )   
    hashed_password = get_hashed_password(request.password)
    user = {"username":request.username, "email":request.email, "password":hashed_password}
    users_col.insert_one(user)
    print( type(user))
    return {"status":status.HTTP_201_CREATED}