from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_current_active_user

from routers.users import schemas
from dependencies import get_db
from routers.users import crud, schemas

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/user/status", response_model=schemas.User)
def activate_or_deactivate_user(user: schemas.UserChangeStatus, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(
        db, username=user.username)

    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")

    if not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password is incorrect")

    return crud.change_user_status(db=db, user=db_user)


@router.get("/users/", response_model=list[schemas.User], dependencies=[Depends(get_current_active_user)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print(users)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


