import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Article,
    ArticleCreate,
    ArticlePublic,
    ArticlesPublic,
    ArticleType,
    ArticleUpdate,
    Message,
)

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=ArticlesPublic)
def read_articles(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve artilces.
    """
    count_statement = select(func.count()).select_from(Article)
    count = session.exec(count_statement).one()
    statement = select(Article).offset(skip).limit(limit)
    articles = session.exec(statement).all()
    return ArticlesPublic(data=articles, count=count)


@router.get("/{id}", response_model=ArticlePublic)
def read_article(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get article by ID.
    """
    article = session.get(Article, id)
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    return article


@router.post("/", response_model=ArticlePublic)
def create_article(
    session: SessionDep, current_user: CurrentUser, article_in: ArticleCreate, article_type_id: uuid.UUID
) -> Any:
    """
    Create new article.
    """
    article_type = session.get(ArticleType, article_type_id)
    if not article_type:
        raise HTTPException(status_code=404, detail="Article type not found")
    article = Article.model_validate(article_in, update={"owner_id": current_user.id, "article_type_id": article_type_id})
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


@router.put("/{id}", response_model=ArticlePublic)
def update_article(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    article_in: ArticleUpdate,
) -> Any:
    """
    Update an article.
    """
    article = session.get(Article, id)
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    if not current_user.is_superuser and (article.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = article_in.model_dump(exclude_unset=True)
    article.sqlmodel_update(update_dict)
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


@router.delete("/{id}")
def delete_article(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an article.
    """
    article = session.get(Article, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not current_user.is_superuser and (article.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(article)
    session.commit()
    return Message(message="Article deleted successfully")
