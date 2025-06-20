import datetime
from pydantic import BaseModel, HttpUrl

class SourceBase(BaseModel):
    name: str
    url: HttpUrl

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int
    created_at: datetime.datetime
    class Config:
        from_attributes=True