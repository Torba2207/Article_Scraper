from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..dependencies import get_db

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
    return crud.create_source(db=db, source=source)