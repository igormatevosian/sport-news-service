import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ArticleType,
    ArticleTypeCreate,
    ArticleTypesPublic,
    ArticleTypeUpdate,
    Message,
)

router = APIRouter(prefix="/article_types", tags=["article_types"])


@router.get("/", response_model=ArticleTypesPublic)
def read_article_types(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve artilce types.
    """
    count_statement = select(func.count()).select_from(ArticleType)
    count = session.exec(count_statement).one()
    statement = select(ArticleType).offset(skip).limit(limit)
    article_types = session.exec(statement).all()
    return ArticleTypesPublic(data=article_types, count=count)


@router.get("/{id}", response_model=ArticleType)
def read_article_type(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get article type by ID.
    """
    article_type = session.get(ArticleType, id)
    if not article_type:
        raise HTTPException(status_code=404, detail="Article type not found")
    return article_type


@router.post("/", response_model=ArticleType)
def create_article_type(
    *, session: SessionDep, current_user: CurrentUser, article_in: ArticleTypeCreate
) -> Any:
    """
    Create new article type.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    article_type = ArticleType.model_validate(article_in)
    session.add(article_type)
    session.commit()
    session.refresh(article_type)
    return article_type


@router.put("/{id}", response_model=ArticleType)
def update_article_type(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    article_in: ArticleTypeUpdate,
) -> Any:
    """
    Update an article type.
    """
    article_type = session.get(ArticleType, id)
    if not article_type:
        raise HTTPException(status_code=404, detail="Article type not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = article_in.model_dump(exclude_unset=True)
    article_type.sqlmodel_update(update_dict)
    session.add(article_type)
    session.commit()
    session.refresh(article_type)
    return article_type


@router.delete("/{id}")
def delete_article_type(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an article type.
    """
    article_type = session.get(ArticleType, id)
    if not article_type:
        raise HTTPException(status_code=404, detail="Article type not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(article_type)
    session.commit()
    return Message(message="Article type deleted successfully")
