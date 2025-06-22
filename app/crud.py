from sqlalchemy.orm import Session
from . import models
from . import schemas
import datetime


def get_source(db: Session, source_id: int):
    return db.query(models.Source).filter(models.Source.id == source_id).first()

def get_source_by_name(db: Session, name: str):
    return db.query(models.Source).filter(models.Source.name == name).first()

def get_source_by_url(db: Session, url: str):
    return db.query(models.Source).filter(models.Source.url == url).first()

def get_sources(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Source).offset(skip).limit(limit).all()

def create_source(db: Session, source: schemas.SourceCreate):
    db_source = models.Source(name=source.name, url=str(source.url))
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()

def delete_article(db: Session, article_id: int):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
        return article
    return None

def scrape_article(db: Session, article: schemas.ArticleCreate, source_id: int):
    db_article = models.Article(
        title=article.title,
        content=article.content,
        source_id=source_id,
        scraped_at=datetime.datetime.now()  # Explicitly set the time
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article