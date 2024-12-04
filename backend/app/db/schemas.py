from datetime import datetime

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    short_description: str | None = None
    description: str | None = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    owner_id: int
    article_type_id: int
    created_date: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    name: str | None = None
    picture: str | None = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    articles: list[Article] = []

    class Config:
        from_attributes = True


class ArticleTypeBase(BaseModel):
    name: str


class ArticleTypeCreate(ArticleTypeBase):
    pass


class ArticleType(ArticleTypeBase):
    id: int

    class Config:
        from_attributes = True


class ArticleCommentBase(BaseModel):
    content: str


class ArticleCommentCreate(ArticleCommentBase):
    pass


class ArticleComment(ArticleCommentBase):
    id: int
    article_id: int
    commenter_id: int
    created_date: datetime

    class Config:
        from_attributes = True
