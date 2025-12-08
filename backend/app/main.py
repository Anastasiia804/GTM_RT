from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import advertisers, scripts, loader, health

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Tag Manager System API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(advertisers.router)
app.include_router(scripts.router)
app.include_router(loader.router)
app.include_router(health.router)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "TSPRTG Tag Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api")
def api_root():
    """API root endpoint"""
    return {
        "message": "TSPRTG Tag Manager API",
        "endpoints": {
            "advertisers": "/api/advertisers",
            "scripts": "/api/scripts",
            "health": "/api/health",
            "loader": "/c/{container_id}/l.js"
        }
    }
