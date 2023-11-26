from fastapi import Depends, APIRouter
from dependencies import get_db, get_current_active_user
from routers.items import schemas, crud
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: UUID, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)
