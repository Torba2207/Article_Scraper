import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .source import Source  # Avoid circular import issues


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str| None] = mapped_column(Text, nullable=True)

    scraped_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))

    source: Mapped["Source"] = relationship(back_populates="articles")