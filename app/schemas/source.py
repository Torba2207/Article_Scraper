import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict


class SourceBase(BaseModel):
    name: str
    url: HttpUrl

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
