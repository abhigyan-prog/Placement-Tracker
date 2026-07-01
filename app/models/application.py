from datetime import date, datetime
from uuid import UUID
from enum import Enum
from sqlalchemy import UUID as PG_UUID,Date,DateTime,Enum as PG_Enum,ForeignKey,String,func,text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from ..database import Base
if TYPE_CHECKING:
    from .user import User
    from .company import Company
    from .resume import Resume
    from .note import Note

class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    OA = "OA"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    OFFER = "Offer"

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    company_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="RESTRICT"),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    application_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        PG_Enum(ApplicationStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        server_default=text("'Applied'"),
        index=True,
    )

    resume_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="SET NULL"),
        nullable=True,
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
        back_populates="applications"
    )

    company: Mapped["Company"] = relationship(
        back_populates="applications"
    )

    resume: Mapped["Resume"] = relationship(
        back_populates="applications"
    )
    notes:Mapped[list["Note"]]=relationship(
        back_populates="application"
    )
