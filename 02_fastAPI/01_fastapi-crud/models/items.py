from sqlalchemy import Column, Integer, String
from db.base import Base

class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100))
    item_detail = Column(String(150), unique=True)