import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from starlette.middleware.sessions import SessionMiddleware

from app.db import models
from app.db.db import engine
from app.routers import (
    article_comments,
    article_types,
    articles,
    pages,
    security,
    sockets,
    users,
)

load_dotenv()

app = FastAPI()
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(article_types.router)
app.include_router(article_comments.router)
app.include_router(security.router)
app.include_router(pages.router)
app.include_router(sockets.router)

SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
