from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

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
