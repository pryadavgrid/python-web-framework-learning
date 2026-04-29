from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.items import ItemCreate, ItemResponse
from services.item_service import (
    create_items_service,
    update_items_service, 
    delete_item_service
)
from crud.items import get_items, get_item_by_id

router = APIRouter()


# CREATE
@router.post("/", response_model=ItemResponse)
def create_items(item: ItemCreate, db: Session = Depends(get_db)):
    return create_items_service(db, item.item_name, item.item_detail)



# READ ALL
@router.get("/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)