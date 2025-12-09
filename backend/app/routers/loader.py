from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
import json
from urllib.parse import urlparse

from ..database import get_db
from ..models.advertiser import Advertiser
from ..models.health_log import HealthLog
from ..services.container_generator import generate_loader_script, minify_js

router = APIRouter(tags=["loader"])


def is_domain_allowed(referer: str, allowed_domains: list) -> bool:
    """Check if referer domain is in allowed domains list"""
    if not referer:
        return False
    
    if not allowed_domains:
        return False
    
    try:
        parsed = urlparse(referer)
        referer_domain = parsed.netloc.lower()
        
        # Remove www. prefix for comparison
        if referer_domain.startswith('www.'):
            referer_domain = referer_domain[4:]
        
        for allowed in allowed_domains:
            allowed = allowed.lower()
            if allowed.startswith('www.'):
                allowed = allowed[4:]
            
            # Check exact match or subdomain
            if referer_domain == allowed or referer_domain.endswith('.' + allowed):
                return True
        
        return False
    except:
        return False


@router.get("/c/{container_id}/l.js")
def load_container(
    container_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Public endpoint to load container JavaScript"""
    
    # Get advertiser by container_id
    advertiser = db.query(Advertiser).filter(
        Advertiser.container_id == container_id
    ).first()
    
    # Get request info
    referer = request.headers.get('referer', '')
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get('user-agent', '')
    
    # Default response
    js_code = "// TSPRTG: Container not found or inactive\n"
    is_allowed = False
    
    if advertiser:
        # Parse allowed domains with error handling
        try:
            allowed_domains = json.loads(advertiser.domains) if advertiser.domains else []
        except json.JSONDecodeError:
            # If JSON parsing fails, treat as no domains configured
            allowed_domains = []
        
        # Check if domain is allowed and advertiser is active
        is_allowed = is_domain_allowed(referer, allowed_domains) and advertiser.is_active
        
        if is_allowed:
            # Generate loader script
            js_code = generate_loader_script(db, advertiser)
            # Minify the code
            js_code = minify_js(js_code)
    
    # Log the request
    log_entry = HealthLog(
        container_id=container_id,
        referer=referer,
        ip_address=ip_address,
        user_agent=user_agent,
        is_allowed=is_allowed
    )
    db.add(log_entry)
    db.commit()
    
    # Return JavaScript with appropriate headers
    return Response(
        content=js_code,
        media_type="application/javascript",
        headers={
            "Cache-Control": "public, max-age=300",  # 5 minutes cache
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "*"
        }
    )
