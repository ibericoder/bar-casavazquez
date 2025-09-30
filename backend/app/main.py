from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from .core.config import settings
from .core.database import get_db
from .api import wines, drinks, snacks, notifications, auth
from .routers import chat

app = FastAPI(
    title="Casa Vazquez API",
    description="API for Casa Vazquez restaurant menu management",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Use the property instead
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(wines.router, prefix="/api/wines", tags=["wines"])
app.include_router(drinks.router, prefix="/api/drinks", tags=["drinks"])
app.include_router(snacks.router, prefix="/api/snacks", tags=["snacks"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

# Legacy endpoint for compatibility
app.include_router(wines.router, prefix="/casavazquez/api", tags=["legacy"])

# Static file serving for Vue frontend
website_dist = Path(__file__).parent.parent.parent / "website" / "dist"
if website_dist.exists():
    app.mount("/casavazquez", StaticFiles(directory=str(website_dist)), name="static")

@app.get("/")
async def root():
    return {"message": "Casa Vazquez API v2.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve Vue.js app for all other routes
@app.get("/casavazquez/{full_path:path}")
async def serve_vue_app(full_path: str):
    """Serve the Vue.js app for any route that doesn't match the API"""
    index_path = website_dist / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"error": "Frontend not found"}