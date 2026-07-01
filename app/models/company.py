from datetime import datetime
from uuid import UUID
from sqlalchemy import UUID as PG_UUID, ForeignKey, func,text,String,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from.user import User
    from .application import Application
    from .note import Note

class Company(Base):
    __tablename__="companies"
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable= False,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    ) 
    website: Mapped[str|None] = mapped_column(
        String(500),
        nullable=True
    )
    industry: Mapped[str|None] = mapped_column(
        String(100),
        nullable=True
    )
    created_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at:Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    user: Mapped["User"] = relationship(
        back_populates="companies"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="company"
    )
    notes:Mapped[list["Note"]]=relationship(
        back_populates="company"
    )