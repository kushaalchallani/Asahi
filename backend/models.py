from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

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

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )