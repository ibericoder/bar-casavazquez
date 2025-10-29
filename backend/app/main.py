from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
import os
from pathlib import Path
import logging

from .core.config import settings
from .core.database import get_db, get_async_db
from .api import wines, drinks, snacks, notifications, auth
from .mcp.wine_recommender import WineRecommender
from .middleware import RateLimitMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Casa Vazquez API",
    description="API for Casa Vazquez restaurant menu management",
    version="2.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Temporary chat models and endpoints
class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    recommendations: Optional[List[Dict[str, Any]]] = None
    context: Optional[Dict[str, Any]] = None

@app.post("/api/chat/chat", response_model=ChatResponse)
async def chat_with_bot(chat_message: ChatMessage, db: AsyncSession = Depends(get_async_db)):
    """Temporary chat endpoint for testing that uses WineRecommender."""
    try:
        recommender = WineRecommender()
        result = await recommender.recommend_wines(chat_message.message, db)

        # If the recommender returned an error, surface a friendly message
        if result.get('error'):
            raise Exception(result.get('error'))

        explanation = result.get('explanation') or "Ich habe einige Vorschläge für Sie zusammengestellt."
        recommendations = result.get('recommendations', [])

        return ChatResponse(
            response=explanation,
            recommendations=recommendations,
            context={
                'taste_analysis': result.get('taste_analysis'),
                'total_wines_analyzed': result.get('total_wines_analyzed')
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )

# Middleware
app.add_middleware(RateLimitMiddleware, calls=100, period=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])  # Temporarily disabled

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


@app.get("/api/chat/recommend")
async def recommend_get(message: str, db: AsyncSession = Depends(get_async_db)):
    """Simple GET endpoint to test recommendations without JSON body (dev only)."""
    recommender = WineRecommender()
    result = await recommender.recommend_wines(message, db)
    return result

# Serve Vue.js app for all other routes
@app.get("/casavazquez/{full_path:path}")
async def serve_vue_app(full_path: str):
    """Serve the Vue.js app for any route that doesn't match the API"""
    index_path = website_dist / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"error": "Frontend not found"}