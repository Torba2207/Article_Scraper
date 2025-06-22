from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..dependencies import get_db
from ..services import scraper

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

@router.post("/{source_id}/scrape", response_model=schemas.Article, status_code=status.HTTP_202_ACCEPTED)
def scrape_article_from_source(source_id: int, db: Session = Depends(get_db)):
    source = crud.get_source(db, source_id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    # Call the scraper service to scrape articles from the source
    scraped_data = scraper.scrape_article(str(source.url))
    if not scraped_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to scrape data from the source"
        )
    article_create = schemas.ArticleCreate(
        title=scraped_data.get("title"),
        content=scraped_data.get("content"),
        source_id=source_id
    )

    return crud.scrape_article(db=db, article=article_create, source_id=source_id)