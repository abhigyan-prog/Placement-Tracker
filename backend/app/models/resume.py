from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped ,mapped_column,relationship
from sqlalchemy import UUID as PG_UUID, Boolean, DateTime, ForeignKey, String, func , text
from ..database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .application import Application

class Resume(Base):
    __tablename__ = 'resumes'
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id:Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False
    )
    version_name:Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    file_path:Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    is_active:Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('false')
    )
    uploaded_at:Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    user:Mapped['User']=relationship(
        back_populates="resumes"
    )
    applications: Mapped[list["Application"]] = relationship(
    back_populates="resume"
    )
    

