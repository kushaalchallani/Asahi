from core.database import Base
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, DateTime


class CheckIn(Base):
    __tablename__ = 'check_ins'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    feeling: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    note: Mapped[str|None] = mapped_column (
        String,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )