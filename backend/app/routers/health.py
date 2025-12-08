from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.schemas import HealthStatusResponse, HealthLogResponse
from ..services.health_checker import get_all_containers_health, get_container_logs

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("", response_model=HealthStatusResponse)
def get_health_status(db: Session = Depends(get_db)):
    """Get overall health status of the system"""
    health = get_all_containers_health(db)
    return HealthStatusResponse(**health)


@router.get("/containers")
def get_containers_health(db: Session = Depends(get_db)):
    """Get health status of all containers with detailed stats"""
    from ..models.advertiser import Advertiser
    from ..services.health_checker import get_container_stats
    
    advertisers = db.query(Advertiser).all()
    
    containers_health = []
    for advertiser in advertisers:
        stats = get_container_stats(db, advertiser.container_id)
        containers_health.append({
            "advertiser_id": advertiser.id,
            "advertiser_name": advertiser.name,
            **stats
        })
    
    return containers_health


@router.get("/containers/{advertiser_id}/logs", response_model=List[HealthLogResponse])
def get_advertiser_logs(advertiser_id: int, db: Session = Depends(get_db)):
    """Get logs for a specific advertiser's container"""
    from ..models.advertiser import Advertiser
    
    advertiser = db.query(Advertiser).filter(Advertiser.id == advertiser_id).first()
    
    if not advertiser:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Advertiser not found")
    
    logs = get_container_logs(db, advertiser.container_id, limit=100)
    
    return logs
