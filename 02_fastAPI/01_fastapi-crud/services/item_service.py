from sqlalchemy.orm import Session
from fastapi import HTTPException

from crud.items import create_items, update_items, delete_items 


def create_items_service(db: Session, item_name: str, item_detail: str):

    return create_items(db, item_name, item_detail)


def update_items_service(db: Session, item_id: int, item_name: str = None, item_detail: str = None):
    item = update_items(db, item_id, item_name, item_detail)

    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return item


def delete_item_service(db: Session, item_id: int):
    item = delete_items(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}