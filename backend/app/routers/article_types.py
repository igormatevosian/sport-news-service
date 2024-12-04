from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import schemas, services
from app.dependencies import get_db

router = APIRouter(prefix="/article_types", tags=["article_types"])




@router.get("/", response_model=list[schemas.ArticleType])
def read_article_types(
skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of article types.

    - **skip**: Number of article types to skip.
    - **limit**: Maximum number of article types to return.
    - **db**: Database session dependency.

    Returns:
    - List of article types.
    """
    article_type_service = services.ArticleTypeService(db)
    return article_type_service.get_article_types(skip=skip, limit=limit)


@router.post(
    "/",
    response_model=schemas.ArticleType,
    responses={400: {"description": "Operation forbidden"}},
)
def create_article_type(

    article_type: schemas.ArticleTypeCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new article type.

    - **article_type**: Details of the article type to be created.
    - **db**: Database session dependency.

    Returns:
    - **201 Created**: Article type created successfully.
    - **400 Bad Request**: If article type with provided name already exists.
    """
    article_type_service = services.ArticleTypeService(db)
    return article_type_service.create_article_type(article_type)


@router.delete("/{article_type_id}", response_model=bool)
def delete_article_type(
article_type_id: int, db: Session = Depends(get_db)
):
    """
    Delete article type by ID.

    - **article_type_id**: ID of the article type to delete.
    - **db**: Database session dependency.

    Returns:
    - **True**: Article type deleted successfully.
    - **False**: If article type with provided ID does not exist.
    """
    article_type_service = services.ArticleTypeService(db)
    result = article_type_service.delete_article_type(article_type_id)
    if not result:
        raise HTTPException(status_code=404, detail="Article type not found")
    return result
