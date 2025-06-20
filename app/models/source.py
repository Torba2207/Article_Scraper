import datetime
from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .article import Article  # Avoid circular import issues

class Source(Base):
    __tablename__="sources"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    url: Mapped[str]= mapped_column(String(255))
    created_at: Mapped[datetime.datetime]= mapped_column(
        DateTime,
        server_default=func.now()
    )

    articles: Mapped[List["Article"]] = relationship(back_populates="source")