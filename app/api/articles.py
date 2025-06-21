from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)
@router.get("/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = Query(default=100, le=1000), db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles
@router.get("/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article(db, article_id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article
@router.delete("/{article_id}", response_model=schemas.Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.delete_article(db, article_id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article