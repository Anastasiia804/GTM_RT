from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.script import Script
from ..schemas.schemas import ScriptCreate, ScriptUpdate, ScriptResponse

router = APIRouter(prefix="/api/scripts", tags=["scripts"])


@router.get("", response_model=List[ScriptResponse])
def list_global_scripts(db: Session = Depends(get_db)):
    """Get list of all global scripts (advertiser_id is NULL)"""
    scripts = db.query(Script).filter(Script.advertiser_id.is_(None)).all()
    return scripts


@router.post("", response_model=ScriptResponse)
def create_script(script: ScriptCreate, db: Session = Depends(get_db)):
    """Create a new script"""
    
    db_script = Script(
        advertiser_id=script.advertiser_id,
        name=script.name,
        script_type=script.script_type,
        content=script.content,
        is_enabled=script.is_enabled,
        priority=script.priority,
        is_async=script.is_async,
        is_defer=script.is_defer
    )
    
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    
    return db_script


@router.get("/{script_id}", response_model=ScriptResponse)
def get_script(script_id: int, db: Session = Depends(get_db)):
    """Get a specific script"""
    script = db.query(Script).filter(Script.id == script_id).first()
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    return script


@router.put("/{script_id}", response_model=ScriptResponse)
def update_script(
    script_id: int,
    script_update: ScriptUpdate,
    db: Session = Depends(get_db)
):
    """Update a script"""
    db_script = db.query(Script).filter(Script.id == script_id).first()
    
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    # Update fields
    if script_update.name is not None:
        db_script.name = script_update.name
    if script_update.script_type is not None:
        db_script.script_type = script_update.script_type
    if script_update.content is not None:
        db_script.content = script_update.content
    if script_update.is_enabled is not None:
        db_script.is_enabled = script_update.is_enabled
    if script_update.priority is not None:
        db_script.priority = script_update.priority
    if script_update.is_async is not None:
        db_script.is_async = script_update.is_async
    if script_update.is_defer is not None:
        db_script.is_defer = script_update.is_defer
    
    db.commit()
    db.refresh(db_script)
    
    return db_script


@router.delete("/{script_id}")
def delete_script(script_id: int, db: Session = Depends(get_db)):
    """Delete a script"""
    db_script = db.query(Script).filter(Script.id == script_id).first()
    
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    db.delete(db_script)
    db.commit()
    
    return {"message": "Script deleted successfully"}


@router.patch("/{script_id}/toggle", response_model=ScriptResponse)
def toggle_script(script_id: int, db: Session = Depends(get_db)):
    """Toggle script enabled/disabled status"""
    db_script = db.query(Script).filter(Script.id == script_id).first()
    
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    db_script.is_enabled = not db_script.is_enabled
    db.commit()
    db.refresh(db_script)
    
    return db_script


# Advertiser-specific scripts endpoints
@router.get("/advertisers/{advertiser_id}/scripts", response_model=List[ScriptResponse], tags=["advertiser-scripts"])
def list_advertiser_scripts(advertiser_id: int, db: Session = Depends(get_db)):
    """Get list of scripts for a specific advertiser"""
    scripts = db.query(Script).filter(Script.advertiser_id == advertiser_id).all()
    return scripts


@router.post("/advertisers/{advertiser_id}/scripts", response_model=ScriptResponse, tags=["advertiser-scripts"])
def create_advertiser_script(advertiser_id: int, script: ScriptCreate, db: Session = Depends(get_db)):
    """Create a new script for a specific advertiser"""
    
    db_script = Script(
        advertiser_id=advertiser_id,
        name=script.name,
        script_type=script.script_type,
        content=script.content,
        is_enabled=script.is_enabled,
        priority=script.priority,
        is_async=script.is_async,
        is_defer=script.is_defer
    )
    
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    
    return db_script


@router.put("/advertisers/{advertiser_id}/scripts/{script_id}", response_model=ScriptResponse, tags=["advertiser-scripts"])
def update_advertiser_script(
    advertiser_id: int,
    script_id: int,
    script_update: ScriptUpdate,
    db: Session = Depends(get_db)
):
    """Update a script for a specific advertiser"""
    db_script = db.query(Script).filter(
        Script.id == script_id,
        Script.advertiser_id == advertiser_id
    ).first()
    
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    # Update fields
    if script_update.name is not None:
        db_script.name = script_update.name
    if script_update.script_type is not None:
        db_script.script_type = script_update.script_type
    if script_update.content is not None:
        db_script.content = script_update.content
    if script_update.is_enabled is not None:
        db_script.is_enabled = script_update.is_enabled
    if script_update.priority is not None:
        db_script.priority = script_update.priority
    if script_update.is_async is not None:
        db_script.is_async = script_update.is_async
    if script_update.is_defer is not None:
        db_script.is_defer = script_update.is_defer
    
    db.commit()
    db.refresh(db_script)
    
    return db_script


@router.delete("/advertisers/{advertiser_id}/scripts/{script_id}", tags=["advertiser-scripts"])
def delete_advertiser_script(advertiser_id: int, script_id: int, db: Session = Depends(get_db)):
    """Delete a script for a specific advertiser"""
    db_script = db.query(Script).filter(
        Script.id == script_id,
        Script.advertiser_id == advertiser_id
    ).first()
    
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    db.delete(db_script)
    db.commit()
    
    return {"message": "Script deleted successfully"}


@router.patch("/advertisers/{advertiser_id}/scripts/{script_id}/toggle", response_model=ScriptResponse, tags=["advertiser-scripts"])
def toggle_advertiser_script(advertiser_id: int, script_id: int, db: Session = Depends(get_db)):
    """Toggle script enabled/disabled status for advertiser"""
    db_script = db.query(Script).filter(
        Script.id == script_id,
        Script.advertiser_id == advertiser_id
    ).first()
    
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    db_script.is_enabled = not db_script.is_enabled
    db.commit()
    db.refresh(db_script)
    
    return db_script
