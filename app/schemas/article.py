import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional
from .source import Source as SourceSchema

class ArticleBase(BaseModel):
    title: str
    content: Optional[str] = None

class ArticleCreate(ArticleBase):
    source_id: int

class Article(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scraped_at: datetime.datetime
    source: SourceSchema

