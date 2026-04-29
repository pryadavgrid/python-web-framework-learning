from fastapi import FastAPI

from db.base import Base
from db.session import engine
from api.v1.router import api_router

from models import user  # ensures model registration

app = FastAPI(title="FastAPI Project")

# include routes
app.include_router(api_router)

# create tables
Base.metadata.create_all(bind=engine)

# Default route
@app.get("/")
def root():
    return {"message": "API is running"}