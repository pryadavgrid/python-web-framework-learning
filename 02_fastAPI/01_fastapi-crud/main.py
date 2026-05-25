from fastapi import FastAPI, Request

from db.base import Base
from db.session import engine
from api.v1.router import api_router

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from models import user  # ensures model registration

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Project")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes
app.include_router(api_router)

# create tables
Base.metadata.create_all(bind=engine)

# Default route
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request, "index.html")