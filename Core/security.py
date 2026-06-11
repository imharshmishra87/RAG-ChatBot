from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from .config import settings
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

oauth_scheme=OAuth2PasswordBearer(tokenUrl="login",auto_error=False)

pwd_context=CryptContext(schemes=['bcrypt'], deprecated="auto")

def generatehash(password:str)->str:
    hash_password=pwd_context.hash(password)
    return hash_password

def verifyhash(password:str, hash_password:str)->bool:
    return pwd_context.verify(password,hash_password)


def create_access_tokens(data:dict, expire_time:timedelta)->str:
    to_encode=data.copy()

    if expire_time:
        expire=datetime.now(timezone.utc)+ expire_time
    else:
        expire=datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_time)

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

def get_current_user(token:str=Depends(get_token_from_cookies)):
    try:
        payload=jwt.decode(token=token,key=settings.secret_key,algorithms=[settings.algorithm])

        user_id=payload.get("sub")
        role=payload.get("role")

        if user_id is None:
            raise HTTPException(
                detail="Invalid Token",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return {"user_id":user_id,"role":role}
    except JWTError:
        raise HTTPException(
            detail="Token is unauthorised or expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
def required_role(required_role:str):
    def role_checker(current_user:str=Depends(get_current_user)):
        if required_role!=current_user['role']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this route"
            )
        return current_user
    return role_checker



