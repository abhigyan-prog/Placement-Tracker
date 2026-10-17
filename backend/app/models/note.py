from enum import Enum
from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import UUID as PG_UUID,String,DateTime,Enum as PG_Enum, ForeignKey, Text, func, text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .application import Application
    from .company import Company
    from .user import User


class NoteType(str, Enum):
    GENERAL = "general"
    INTERVIEW_PREP = "interview_prep"
    OA_PREP = "oa_prep"
    COMPANY_SPECIFIC = "company_specific"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    application_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=True,
    )

    company_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
    )

    note_type: Mapped[NoteType] = mapped_column(
        PG_Enum(NoteType, name="note_type", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        server_default=text("'general'"),
    )
    title : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
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

    user: Mapped["User"] = relationship(
        back_populates="notes"
    )

    company: Mapped["Company"] = relationship(
        back_populates="notes"
    )

    application: Mapped["Application"] = relationship(
        back_populates="notes"
    )