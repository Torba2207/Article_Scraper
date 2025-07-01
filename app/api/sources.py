from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..dependencies import get_db
from ..services import ArticleScraper



router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)

@router.get("/", response_model=List[schemas.Source])
def read_sources(skip: int = 0, limit: int = Query(default=100, le=1000), db: Session = Depends(get_db)):
    sources = crud.get_sources(db, skip=skip, limit=limit)
    return sources

@router.get("/{source_id}", response_model=schemas.Source)
def read_source(source_id: int, db: Session = Depends(get_db)):
    source = crud.get_source(db, source_id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    return source




@router.post("/", response_model=schemas.Source, status_code=status.HTTP_201_CREATED)
def create_new_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    db_source = crud.get_source_by_name(db,name=source.name)
    if db_source:
        raise HTTPException(status_code=400, detail=f"Source with name '{source.name}' already registered")
    db_source_by_url = crud.get_source_by_url(db, url=str(source.url))
    if db_source_by_url:
        raise HTTPException(status_code=400, detail=f"Source with URL '{source.url}' already registered")
    return crud.create_source(db=db, source=source)

@router.post("/{source_id}/scrape", response_model=schemas.ScrapedArticlesResponse, status_code=status.HTTP_202_ACCEPTED)
def scrape_article_from_source(source_id: int, db: Session = Depends(get_db)):
    source = crud.get_source(db, source_id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    with ArticleScraper.ArticleScraper() as scraper:
        scraped_articles = scraper.crawl_source(str(source.url))

    if not scraped_articles:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to scrape article from source"
        )
    saved_count = 0
    for article in scraped_articles:
        db_article = schemas.ArticleCreate(title=article['title'], content=article['content'], source_id=source_id)
        saved_article = crud.scrape_article(db=db, article=db_article, source_id=source_id)
        if saved_article:
            saved_count += 1

    return {
        "message": f"Successfully scraped and saved {saved_count} articles from source '{source.name}'",
        "source_id": source_id,
        "scraped_articles": scraped_articles
    }