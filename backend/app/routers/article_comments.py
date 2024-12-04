from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db import services, schemas
from app.dependencies import get_db


router = APIRouter(prefix="/article_comments", tags=["article_comments"])

limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=list[schemas.ArticleComment])
@limiter.limit("1000/minute")
def read_article_comments(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of article comments.

    - **skip**: Number of article comments to skip.
    - **limit**: Maximum number of article comments to return.
    - **db**: Database session dependency.

    Returns:
    - List of article comments.
    """
    article_comment_service = services.ArticleCommentService(db)
    return article_comment_service.get_article_comments(skip=skip, limit=limit)


@router.get("/article/{article_id}", response_model=list[schemas.ArticleComment])
@limiter.limit("1000/minute")
def read_article_comments_by_article_id(request: Request, article_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve article comments by article ID.

    - **article_id**: ID of the article whose comments to retrieve.
    - **skip**: Number of article comments to skip.
    - **limit**: Maximum number of article comments to return.
    - **db**: Database session dependency.

    Returns:
    - List of article comments belonging to the specified article.
    """
    article_comment_service = services.ArticleCommentService(db)
    return article_comment_service.get_article_comments_by_article_id(article_id, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=list[schemas.ArticleComment])
@limiter.limit("1000/minute")
def read_article_comments_by_user_id(request: Request, user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve article comments by user ID.

    - **user_id**: ID of the user whose comments to retrieve.
    - **skip**: Number of article comments to skip.
    - **limit**: Maximum number of article comments to return.
    - **db**: Database session dependency.

    Returns:
    - List of article comments posted by the specified user.
    """
    article_comment_service = services.ArticleCommentService(db)
    return article_comment_service.get_article_comments_by_user_id(user_id, skip=skip, limit=limit)


@router.post("/", response_model=schemas.ArticleComment)
@limiter.limit("1000/minute")
def create_article_comment(request: Request, comment: schemas.ArticleCommentCreate, article_id: int, commenter_id: int, db: Session = Depends(get_db)):
    """
    Create a new article comment.

    - **comment**: Details of the article comment to be created.
    - **article_id**: ID of the article the comment belongs to.
    - **commenter_id**: ID of the user posting the comment.
    - **db**: Database session dependency.

    Returns:
    - **201 Created**: Article comment created successfully.
    """
    article_comment_service = services.ArticleCommentService(db)
    return article_comment_service.create_article_comment(comment, article_id, commenter_id)


@router.delete("/{comment_id}", response_model=bool)
@limiter.limit("1000/minute")
def delete_article_comment(request: Request, comment_id: int, db: Session = Depends(get_db)):
    """
    Delete article comment by ID.

    - **comment_id**: ID of the article comment to delete.
    - **db**: Database session dependency.

    Returns:
    - **True**: Article comment deleted successfully.
    - **False**: If article comment with provided ID does not exist.
    """
    article_comment_service = services.ArticleCommentService(db)
    result = article_comment_service.delete_article_comment(comment_id)
    if not result:
        raise HTTPException(
            status_code=404, detail="Article comment not found")
    return result
