import datetime
from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database import Base

class Source(Base):
    __tablename__="sources"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    url: Mapped[str]
    created_at: Mapped[datetime.datetime]= mapped_column(
        DateTime,
        server_default=func.now()
    )