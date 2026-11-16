from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    email: Mapped[str] = mapped_column(
        String(320), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    difficulty_preference: Mapped[str] = mapped_column(
        String(20), default="moderate", nullable=False
    )
    name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    # Settings
    theme: Mapped[str] = mapped_column(
        String(10), default="system", nullable=False
    )
    reminders_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    reminder_time: Mapped[str] = mapped_column(
        String(5), default="20:00", nullable=False
    )
    email_digest: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    text_size: Mapped[str] = mapped_column(
        String(10), default="normal", nullable=False
    )
    reduced_motion: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    high_contrast: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )