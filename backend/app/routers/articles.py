from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import schemas, services
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/articles", tags=["articles"])



@router.post(
    "/",
    response_model=schemas.Article,
    responses={400: {"description": "Operation forbidden"}},
)
def create_article(
    request: Request,
    article_type_id: int,
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new article.

    - **article_type_id**: ID of the article type.
    - **article**: Details of the article to be created.
    - **db**: Database session dependency.

    Returns:
    - **201 Created**: Article created successfully.
    - **400 Bad Request**: If article type with provided ID does not exist or if user already created article with provided title.
    """
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")
    article_service = services.ArticleService(db)
    return article_service.create_user_article(
        user_id=user.id, article_type_id=article_type_id, article=article
    )


@router.get("/", response_model=list[schemas.Article])
def read_articles(
skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of articles.

    - **skip**: Number of articles to skip.
    - **limit**: Maximum number of articles to return.
    - **db**: Database session dependency.

    Returns:
    - List of articles.
    """
    article_service = services.ArticleService(db)
    return article_service.get_articles(skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=list[schemas.Article])
def read_articles_by_user_id(

    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve articles by user ID.

    - **user_id**: ID of the user whose articles to retrieve.
    - **skip**: Number of articles to skip.
    - **limit**: Maximum number of articles to return.
    - **db**: Database session dependency.

    Returns:
    - List of articles belonging to the specified user.
    """
    article_service = services.ArticleService(db)
    return article_service.get_articles_by_user_id(user_id, skip=skip, limit=limit)


@router.get("/article_type/{article_type_id}", response_model=list[schemas.Article])
def read_articles_by_article_type_id(
    article_type_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve articles by article type ID.

    - **article_type_id**: ID of the article type whose articles to retrieve.
    - **skip**: Number of articles to skip.
    - **limit**: Maximum number of articles to return.
    - **db**: Database session dependency.

    Returns:
    - List of articles belonging to the specified article type.
    """
    article_service = services.ArticleService(db)
    return article_service.get_articles_by_article_type_id(
        article_type_id, skip=skip, limit=limit
    )


@router.delete("/{article_id}", response_model=bool)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """
    Delete article by ID.

    - **article_id**: ID of the article to delete.
    - **db**: Database session dependency.

    Returns:
    - **True**: Article deleted successfully.
    - **False**: If article with provided ID does not exist.
    """
    article_service = services.ArticleService(db)
    result = article_service.delete_article(article_id)
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return result
