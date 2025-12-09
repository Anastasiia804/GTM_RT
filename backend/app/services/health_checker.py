from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models.advertiser import Advertiser
from ..models.health_log import HealthLog
from datetime import datetime, timedelta
from typing import Dict, List


def get_container_stats(db: Session, container_id: str) -> Dict:
    """Get statistics for a specific container"""
    
    # Get the advertiser
    advertiser = db.query(Advertiser).filter(Advertiser.container_id == container_id).first()
    if not advertiser:
        return None
    
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)
    one_week_ago = now - timedelta(days=7)
    
    # Count loads today
    loads_today = db.query(func.count(HealthLog.id)).filter(
        HealthLog.container_id == container_id,
        HealthLog.created_at >= one_day_ago
    ).scalar()
    
    # Count loads this week
    loads_week = db.query(func.count(HealthLog.id)).filter(
        HealthLog.container_id == container_id,
        HealthLog.created_at >= one_week_ago
    ).scalar()
    
    # Get last load time
    last_log = db.query(HealthLog).filter(
        HealthLog.container_id == container_id
    ).order_by(HealthLog.created_at.desc()).first()
    
    last_load = last_log.created_at if last_log else None
    
    # Determine status
    if not last_log:
        status = 'never'
    elif last_load and last_load >= one_day_ago:
        status = 'active'
    else:
        status = 'inactive'
    
    return {
        'container_id': container_id,
        'loads_today': loads_today,
        'loads_week': loads_week,
        'last_load': last_load,
        'status': status
    }


def get_all_containers_health(db: Session) -> Dict:
    """Get health status of all containers"""
    
    advertisers = db.query(Advertiser).all()
    
    total_containers = len(advertisers)
    active_containers = 0
    inactive_containers = 0
    never_loaded_containers = 0
    
    for advertiser in advertisers:
        stats = get_container_stats(db, advertiser.container_id)
        if stats['status'] == 'active':
            active_containers += 1
        elif stats['status'] == 'inactive':
            inactive_containers += 1
        else:
            never_loaded_containers += 1
    
    return {
        'status': 'ok',
        'total_containers': total_containers,
        'active_containers': active_containers,
        'inactive_containers': inactive_containers,
        'never_loaded_containers': never_loaded_containers
    }


def get_container_logs(db: Session, container_id: str, limit: int = 100) -> List[HealthLog]:
    """Get recent logs for a container"""
    
    logs = db.query(HealthLog).filter(
        HealthLog.container_id == container_id
    ).order_by(HealthLog.created_at.desc()).limit(limit).all()
    
    return logs
