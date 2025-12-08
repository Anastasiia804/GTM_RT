from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(String, nullable=False, index=True)
    referer = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    is_allowed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
