from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    advertiser_id = Column(Integer, ForeignKey('advertisers.id', ondelete='CASCADE'), nullable=True)
    name = Column(String, nullable=False)
    script_type = Column(String, nullable=False)  # 'external' or 'inline'
    content = Column(Text, nullable=False)  # URL or code
    is_enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Lower number = higher priority
    is_async = Column(Boolean, default=True)
    is_defer = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
