from pydantic import BaseModel
from typing import Optional
from .source import Source as SourceSchema

class ArticleBase(BaseModel):
    title: str
    content: Optional[str] = None

class ArticleCreate(ArticleBase):
    source_id: int

class Article(ArticleBase):
    id: int
    scraped_at: str
    source: SourceSchema

    class Config:
        from_attributes = True
