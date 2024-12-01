from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    picture = Column(String)
    is_active = Column(Boolean, default=True)
    articles = relationship("Article", back_populates="owner")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    short_description = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="articles")
    article_type_id = Column(Integer, ForeignKey("article_type.id"))
    created_date = Column(DateTime, default=datetime.now)
    comments = relationship("ArticleComment", back_populates="article")


class ArticleType(Base):
    __tablename__ = "article_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class ArticleComment(Base):
    __tablename__ = "article_comments"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="comments")
    commenter_id = Column(Integer, ForeignKey("users.id"))
    commenter = relationship("User")
    content = Column(String)
    created_date = Column(DateTime, default=datetime.now)
