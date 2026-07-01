from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, func, text,UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..database import Base
if TYPE_CHECKING:
    from .company import Company
    from .application import Application
    from .resume import Resume
    from .note import Note

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('true'),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    companies: Mapped[list["Company"]] = relationship(
    back_populates="user"
    )
    applications: Mapped[list["Application"]] = relationship(
    back_populates="user"
    )
    resumes: Mapped[list["Resume"]]=relationship(
        back_populates="user"
    )
    notes:Mapped[list["Note"]]=relationship(
        back_populates="user"
    )
    