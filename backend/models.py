from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean
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

    note: Mapped[str|None] = mapped_column (
        String,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            index=True
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    difficulty: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    social_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    energy_required: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


class UserMission(Base):
    __tablename__ = 'user_missions'

    id: Mapped[int] = mapped_column(
                Integer,
                primary_key=True,
                index=True
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

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
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