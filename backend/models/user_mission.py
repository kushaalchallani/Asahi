from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, String, Integer
from datetime import datetime

class UserMission(Base):
    __tablename__ = 'user_missions'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    mission_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="assigned"
    )

    feedback: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    feedback_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    started_at: Mapped[datetime|None] = mapped_column(
        DateTime,
        nullable=True
    )

    completed_at: Mapped[datetime|None] =  mapped_column(
        DateTime,
        nullable=True
    )