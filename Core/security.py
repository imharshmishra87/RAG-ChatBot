from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta, timezone
from .config import settings
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from Core.database import get_db
from sqlalchemy.orm import Session
from Model import model
oauth_scheme=OAuth2PasswordBearer(tokenUrl="/login",auto_error=False)



def generatehash(password:str)->str:
    pwd_bytes=password.encode("utf-8")
    salt=bcrypt.gensalt()
    hash_password=bcrypt.hashpw(pwd_bytes,salt)
    return hash_password.decode("utf-8")
    

def verifyhash(password:str, hash_password:str)->bool:
    pwd_bytes=password.encode("utf-8")
    hash_bytes=hash_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes,hash_bytes)


def create_access_tokens(data:dict, expire_time:timedelta)->str:
    to_encode=data.copy()

    if expire_time:
        expire=datetime.now(timezone.utc)+ expire_time
    else:
        expire=datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_time)

    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,settings.secret_key,settings.algorithm)

    return encoded_jwt

def create_refresh_token(data:dict, expire_time:timedelta)->str:
    to_encode=data.copy()

    expire=datetime.now(timezone.utc)+timedelta(days=settings.refresh_token_time)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,settings.secret_key,settings.algorithm)

    return encoded_jwt

def get_token_from_cookies(request:Request, token_from_docs:str=Depends(oauth_scheme))->str:
    token=request.cookies.get("access_token")

    if not token and token_from_docs:
        token=token_from_docs
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication cookies"
        )
    return token

def get_current_user(token:str=Depends(get_token_from_cookies),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token=token,key=settings.secret_key,algorithms=[settings.algorithm])
        print(payload)

        user_id=payload.get("sub")
        role=payload.get("role")
        

        if user_id is None:
            raise HTTPException(
                detail="Invalid Token",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        user_id=int(user_id)
        user=db.query(model.User).filter(model.User.id==user_id).first()
        
        if user is None:
            raise HTTPException(
                detail="User does not exists",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return user
    except JWTError as e:
        raise HTTPException(
            detail=f"Token is unauthorised or expired--{e}",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
def required_role(required_role:str):
    def role_checker(current_user:str=Depends(get_current_user)):
        if required_role!=current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this route"
            )
        return current_user
    return role_checker



