from sqlalchemy.orm import Session
from . import models, schemas


# Операции CRUD для модели User
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# Операции CRUD для модели Article
def get_article_by_id(db: Session, id: int):
    return db.query(models.Article).filter(models.Article.id == id).first()


def get_article_by_user_id_and_title(db: Session, user_id: int, title: str):
    return db.query(models.Article).filter(models.Article.owner_id == user_id, models.Article.title == title).first()


def get_articles_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Article).filter(models.Article.owner_id == user_id).order_by(models.Article.id.desc()).offset(skip).limit(limit).all()


def get_articles_by_article_type_id(db: Session, article_type_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Article).filter(models.Article.article_type_id == article_type_id).order_by(models.Article.id.desc()).offset(skip).limit(limit).all()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).order_by(models.Article.id.desc()).offset(skip).limit(limit).all()


def create_user_article(db: Session, article: schemas.ArticleCreate, user_id: int, article_type_id: int):
    db_article = models.Article(
        **article.model_dump(), owner_id=user_id, article_type_id=article_type_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
        return True
    return False


# Операции CRUD для модели ArticleType
def get_article_type_by_id(db: Session, article_type_id: int):
    return db.query(models.ArticleType).filter(models.ArticleType.id == article_type_id).first()


def get_article_type_by_name(db: Session, article_type_name: str):
    return db.query(models.ArticleType).filter(models.ArticleType.name == article_type_name).first()


def get_article_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ArticleType).offset(skip).limit(limit).all()


def create_article_type(db: Session, article_type: schemas.ArticleTypeCreate):
    db_article_type = models.ArticleType(name=article_type.name)
    db.add(db_article_type)
    db.commit()
    db.refresh(db_article_type)
    return db_article_type


def delete_article_type(db: Session, article_type_id: int):
    article_type = db.query(models.ArticleType).filter(
        models.ArticleType.id == article_type_id).first()
    if article_type:
        db.delete(article_type)
        db.commit()
        return True
    return False


# Операции CRUD для модели ArticleComment
def get_article_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ArticleComment).offset(skip).limit(limit).all()


def get_article_comments_by_article_id(db: Session, article_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ArticleComment).filter(models.ArticleComment.article_id == article_id).offset(skip).limit(limit).all()


def get_article_comments_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ArticleComment).filter(models.ArticleComment.commenter_id == user_id).offset(skip).limit(limit).all()


def create_article_comment(db: Session, comment: schemas.ArticleCommentCreate, article_id: int, commenter_id: int):
    db_comment = models.ArticleComment(
        **comment.model_dump(), article_id=article_id, commenter_id=commenter_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_article_comment(db: Session, comment_id: int):
    comment = db.query(models.ArticleComment).filter(
        models.ArticleComment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False
