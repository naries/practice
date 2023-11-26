from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from config import settings
from database import SessionLocal
from routers.security.schemas import TokenData, User
from sqlalchemy.orm import Session
from routers.users import models
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = settings.security.SECRET_KEY
ALGORITHM = settings.security.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not logged in",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="User is disabled")
    return current_user
