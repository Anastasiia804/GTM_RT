from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base
import secrets
import string


def generate_container_id():
    """Generate unique container ID like 'adv_a1b2c3d4'
    Note: Uniqueness is enforced by database UNIQUE constraint on container_id column.
    If collision occurs (extremely rare), database will raise IntegrityError.
    """
    random_str = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"adv_{random_str}"


class Advertiser(Base):
    __tablename__ = "advertisers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    container_id = Column(String, unique=True, nullable=False, default=generate_container_id)
    domains = Column(Text, nullable=False, default="[]")  # JSON list
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
