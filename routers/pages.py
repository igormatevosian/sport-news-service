from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from db import services
from dependencies import get_db, get_current_user, templates, get_article_types

router = APIRouter(tags=["pages"])

limiter = Limiter(key_func=get_remote_address)


@router.get('/')
@limiter.limit("1000/minute")
async def homepage(request: Request):
    user = get_current_user(request)
    article_types = get_article_types()
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": user, "article_types": article_types})


@router.get('/articles_with_type/{article_type_id}')
@limiter.limit("1000/minute")
async def category_page(request: Request, article_type_id: str):
    user = get_current_user(request)
    article_types = get_article_types()
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": user, "article_types": article_types, "article_type_id": article_type_id})


@router.get('/article_detail/{article_id}')
@limiter.limit("1000/minute")
async def article_detail(request: Request, article_id: int, db: Session = Depends(get_db)):
    user = get_current_user(request)
    article_types = get_article_types()
    article_service = services.ArticleService(db)
    article = article_service.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse("article_detail.html", {"request": request, "article": article, "user": user, "article_types": article_types})


@router.get('/user_page/{user_id}')
@limiter.limit("1000/minute")
async def user_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = get_current_user(request)
    article_types = get_article_types()
    user_service = services.UserService(db)
    author = user_service.get_user(user_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    article_service = services.ArticleService(db)
    articles = article_service.get_articles_by_user_id(user_id)
    is_author = user.id == author.id if user else None
    return templates.TemplateResponse("user_page.html",
                                      {"request": request, "user": user, "articles": articles,
                                       "author": author, "is_author": is_author, "article_types": article_types})


@router.get('/create_article/')
@limiter.limit("1000/minute")
async def create_article(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request)
    article_types = get_article_types()
    return templates.TemplateResponse("create_article.html", {"request": request, "user": user, "article_types": article_types})
