from pydantic import BaseModel

class ItemCreate(BaseModel):
    item_name: str
    item_detail: str

class ItemResponse(BaseModel):
    id: int
    item_name: str
    item_detail: str

    class Config:
        from_attributes = True