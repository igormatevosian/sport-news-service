import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.db import models
from app.db.db import engine
from app.routers import users, articles, article_types, article_comments, security, pages, sockets


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

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
