from sqlalchemy.orm import Session
from . import crud, schemas


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return crud.get_user(self.db, user_id)

    def get_user_by_email(self, email: str):
        return crud.get_user_by_email(self.db, email)

    def get_users(self, skip: int = 0, limit: int = 100):
        return crud.get_users(self.db, skip, limit)

    def create_user(self, user: schemas.UserCreate):
        return crud.create_user(self.db, user)

    def delete_user(self, user_id: int):
        return crud.delete_user(self.db, user_id)


class ArticleService:
    def __init__(self, db: Session):
        self.db = db

    def get_article_by_id(self, id: int):
        return crud.get_article_by_id(self.db, id)

    def get_article_by_user_id_and_title(self, user_id: int, title: str):
        return crud.get_article_by_user_id_and_title(self.db, user_id, title)

    def get_articles_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100):
        return crud.get_articles_by_user_id(self.db, user_id, skip, limit)

    def get_articles_by_article_type_id(self, article_type_id: int, skip: int = 0, limit: int = 100):
        return crud.get_articles_by_article_type_id(self.db, article_type_id, skip, limit)

    def get_articles(self, skip: int = 0, limit: int = 100):
        return crud.get_articles(self.db, skip, limit)

    def create_user_article(self, article: schemas.ArticleCreate, user_id: int, article_type_id: int):
        return crud.create_user_article(self.db, article, user_id, article_type_id)

    def delete_article(self, article_id: int):
        return crud.delete_article(self.db, article_id)


class ArticleTypeService:
    def __init__(self, db: Session):
        self.db = db

    def get_article_type_by_id(self, article_type_id: int):
        return crud.get_article_type_by_id(self.db, article_type_id)

    def get_article_type_by_name(self, article_type_name: str):
        return crud.get_article_type_by_name(self.db, article_type_name)

    def get_article_types(self, skip: int = 0, limit: int = 100):
        return crud.get_article_types(self.db, skip, limit)

    def create_article_type(self, article_type: schemas.ArticleTypeCreate):
        return crud.create_article_type(self.db, article_type)

    def delete_article_type(self, article_type_id: int):
        return crud.delete_article_type(self.db, article_type_id)


class ArticleCommentService:
    def __init__(self, db: Session):
        self.db = db

    def get_article_comments(self, skip: int = 0, limit: int = 100):
        return crud.get_article_comments(self.db, skip, limit)

    def get_article_comments_by_article_id(self, article_id: int, skip: int = 0, limit: int = 100):
        return crud.get_article_comments_by_article_id(self.db, article_id, skip, limit)

    def get_article_comments_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100):
        return crud.get_article_comments_by_user_id(self.db, user_id, skip, limit)

    def create_article_comment(self, comment: schemas.ArticleCommentCreate, article_id: int, commenter_id: int):
        return crud.create_article_comment(self.db, comment, article_id, commenter_id)

    def delete_article_comment(self, comment_id: int):
        return crud.delete_article_comment(self.db, comment_id)
