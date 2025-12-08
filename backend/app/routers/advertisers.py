from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from ..database import get_db
from ..models.advertiser import Advertiser, generate_container_id
from ..schemas.schemas import (
    AdvertiserCreate, AdvertiserUpdate, AdvertiserResponse,
    ContainerCodeResponse, StatsResponse
)
from ..services.container_generator import generate_container_code
from ..services.health_checker import get_container_stats

router = APIRouter(prefix="/api/advertisers", tags=["advertisers"])


@router.get("", response_model=List[AdvertiserResponse])
def list_advertisers(db: Session = Depends(get_db)):
    """Get list of all advertisers"""
    advertisers = db.query(Advertiser).all()
    
    # Convert domains from JSON string to list
    result = []
    for adv in advertisers:
        adv_dict = {
            "id": adv.id,
            "name": adv.name,
            "container_id": adv.container_id,
            "domains": json.loads(adv.domains) if adv.domains else [],
            "is_active": adv.is_active,
            "created_at": adv.created_at,
            "updated_at": adv.updated_at
        }
        result.append(AdvertiserResponse(**adv_dict))
    
    return result


@router.post("", response_model=AdvertiserResponse)
def create_advertiser(advertiser: AdvertiserCreate, db: Session = Depends(get_db)):
    """Create a new advertiser"""
    
    # Create new advertiser
    db_advertiser = Advertiser(
        name=advertiser.name,
        container_id=generate_container_id(),
        domains=json.dumps(advertiser.domains),
        is_active=advertiser.is_active
    )
    
    db.add(db_advertiser)
    db.commit()
    db.refresh(db_advertiser)
    
    return AdvertiserResponse(
        id=db_advertiser.id,
        name=db_advertiser.name,
        container_id=db_advertiser.container_id,
        domains=json.loads(db_advertiser.domains),
        is_active=db_advertiser.is_active,
        created_at=db_advertiser.created_at,
        updated_at=db_advertiser.updated_at
    )


@router.get("/{advertiser_id}", response_model=AdvertiserResponse)
def get_advertiser(advertiser_id: int, db: Session = Depends(get_db)):
    """Get a specific advertiser"""
    advertiser = db.query(Advertiser).filter(Advertiser.id == advertiser_id).first()
    
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    
    return AdvertiserResponse(
        id=advertiser.id,
        name=advertiser.name,
        container_id=advertiser.container_id,
        domains=json.loads(advertiser.domains),
        is_active=advertiser.is_active,
        created_at=advertiser.created_at,
        updated_at=advertiser.updated_at
    )


@router.put("/{advertiser_id}", response_model=AdvertiserResponse)
def update_advertiser(
    advertiser_id: int,
    advertiser_update: AdvertiserUpdate,
    db: Session = Depends(get_db)
):
    """Update an advertiser"""
    db_advertiser = db.query(Advertiser).filter(Advertiser.id == advertiser_id).first()
    
    if not db_advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    
    # Update fields
    if advertiser_update.name is not None:
        db_advertiser.name = advertiser_update.name
    if advertiser_update.domains is not None:
        db_advertiser.domains = json.dumps(advertiser_update.domains)
    if advertiser_update.is_active is not None:
        db_advertiser.is_active = advertiser_update.is_active
    
    db.commit()
    db.refresh(db_advertiser)
    
    return AdvertiserResponse(
        id=db_advertiser.id,
        name=db_advertiser.name,
        container_id=db_advertiser.container_id,
        domains=json.loads(db_advertiser.domains),
        is_active=db_advertiser.is_active,
        created_at=db_advertiser.created_at,
        updated_at=db_advertiser.updated_at
    )


@router.delete("/{advertiser_id}")
def delete_advertiser(advertiser_id: int, db: Session = Depends(get_db)):
    """Delete an advertiser"""
    db_advertiser = db.query(Advertiser).filter(Advertiser.id == advertiser_id).first()
    
    if not db_advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    
    db.delete(db_advertiser)
    db.commit()
    
    return {"message": "Advertiser deleted successfully"}


@router.get("/{advertiser_id}/code", response_model=ContainerCodeResponse)
def get_container_code(advertiser_id: int, db: Session = Depends(get_db)):
    """Get the container embed code for an advertiser"""
    advertiser = db.query(Advertiser).filter(Advertiser.id == advertiser_id).first()
    
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    
    code = generate_container_code(advertiser)
    
    return ContainerCodeResponse(
        container_id=advertiser.container_id,
        code=code
    )


@router.get("/{advertiser_id}/stats", response_model=StatsResponse)
def get_advertiser_stats(advertiser_id: int, db: Session = Depends(get_db)):
    """Get statistics for an advertiser's container"""
    advertiser = db.query(Advertiser).filter(Advertiser.id == advertiser_id).first()
    
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    
    stats = get_container_stats(db, advertiser.container_id)
    
    return StatsResponse(**stats)
