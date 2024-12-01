import os

from fastapi import Request

from db import services
from db.db import SessionLocal
from db.models import User, ArticleType
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request) -> User | None:
    user = request.session.get('user')
    if user:
        db = SessionLocal()
        user_service = services.UserService(db)
        user = user_service.get_user_by_email(user['email'])
        db.close()
        return user


def get_article_types() -> list[ArticleType]:
    db = SessionLocal()
    article_type_service = services.ArticleTypeService(db)
    article_types = article_type_service.get_article_types(limit=5)
    return article_types


config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
