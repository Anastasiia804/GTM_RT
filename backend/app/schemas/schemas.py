from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Advertiser Schemas
class AdvertiserBase(BaseModel):
    name: str
    domains: List[str] = Field(default_factory=list)
    is_active: bool = True


class AdvertiserCreate(AdvertiserBase):
    pass


class AdvertiserUpdate(BaseModel):
    name: Optional[str] = None
    domains: Optional[List[str]] = None
    is_active: Optional[bool] = None


class AdvertiserResponse(AdvertiserBase):
    id: int
    container_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Script Schemas
class ScriptBase(BaseModel):
    name: str
    script_type: str  # 'external' or 'inline'
    content: str
    is_enabled: bool = True
    priority: int = 0
    is_async: bool = True
    is_defer: bool = False


class ScriptCreate(ScriptBase):
    advertiser_id: Optional[int] = None


class ScriptUpdate(BaseModel):
    name: Optional[str] = None
    script_type: Optional[str] = None
    content: Optional[str] = None
    is_enabled: Optional[bool] = None
    priority: Optional[int] = None
    is_async: Optional[bool] = None
    is_defer: Optional[bool] = None


class ScriptResponse(ScriptBase):
    id: int
    advertiser_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Health Log Schemas
class HealthLogResponse(BaseModel):
    id: int
    container_id: str
    referer: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_allowed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Container Code Response
class ContainerCodeResponse(BaseModel):
    container_id: str
    code: str


# Stats Response
class StatsResponse(BaseModel):
    container_id: str
    loads_today: int
    loads_week: int
    last_load: Optional[datetime] = None
    status: str  # 'active', 'inactive', 'never'


# Health Status Response
class HealthStatusResponse(BaseModel):
    status: str
    total_containers: int
    active_containers: int
    inactive_containers: int
    never_loaded_containers: int
