from fastapi import APIRouter
from api.v1.endpoints import users
from api.v1.endpoints import items

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)


api_router.include_router(
    items.router,
    prefix="/items",
    tags=["Items"]
)