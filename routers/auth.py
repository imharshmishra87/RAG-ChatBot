from fastapi import APIRouter, Depends, Cookie, HTTPException,status
from Validation.DataValidation import Register,RegisterResponse  
from jose import jwt ,JWTError,ExpiredSignatureError
from Core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
from Core.security import generatehash, verifyhash, create_access_tokens,create_refresh_token
from sqlalchemy.orm import Session
from Core.database import get_db
from Model import model


router=APIRouter()


@router.post("/register" , response_model=RegisterResponse,response_description="Successfully Registered")
def register_user(data: Register, db:Session=Depends(get_db)):
    email=data.email
    password=data.password.get_secret_value()
    role=data.role
    

    existing_user=db.query(model.User).filter(model.User.email==email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists in the database"
        )
    
    hash=generatehash(password)
    
    new_user=model.User(
        email=email,
        hash=hash,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(response : Response,form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(model.User).filter(model.User.email==form_data.username).first()

    if user is None:
        raise HTTPException(
            detail="The user does not exists in the database",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate":"Bearer"}
        )
    if not verifyhash(form_data.password, user.hash):
        raise HTTPException(
            detail="Invalid Credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate":"Bearer"}
        )
    jwt_payload={
            'sub':str(user.id),
            'role':user.role
    }
    jwt_token=create_access_tokens(jwt_payload,expire_time=None)
    refresh_token=create_refresh_token(jwt_payload,expire_time=None)

    response.set_cookie(
        value=refresh_token,
        key="refresh_token",
        httponly="True",
        secure="True",
        expires=7*24*60*60
    )

    return {"access_token":jwt_token,"token_type":"bearer"}


@router.post("/refresh")
def refresh_access_token(refresh_token:str=Cookie(None), db:Session=Depends(get_db)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token does not exists"
        )
    
    try:
        payload=jwt.decode(refresh_token,key=settings.secret_key,algorithms=[settings.algorithm])
        token_id=payload.get("sub")
        

        if token_id is None:
            raise HTTPException(
                detail="Invalid token payload",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

    except ExpiredSignatureError:
        raise HTTPException(
            detail="Refresh token is expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except JWTError:
        raise HTTPException(
            detail="Invalid refresh token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    user=db.query(model.User).filter(model.User.id==token_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found"
        )
    
    jwt_payload={
        "sub":user.id,
        "role":user.role
    }
    
    new_access_token=create_access_tokens(
        data=jwt_payload,
        expire_time=None
    )

    return {
        "access_token":new_access_token,
        "token_type":"bearer"

    }





    
