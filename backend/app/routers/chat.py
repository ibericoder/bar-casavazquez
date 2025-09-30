from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..core.database import get_db
from ..mcp.wine_recommender import WineRecommender
from ..core.config import settings

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    recommendations: Optional[List[Dict[str, Any]]] = None
    context: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_message: ChatMessage,
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with the wine recommendation bot.
    """
    if not settings.enable_chatbot:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chatbot feature is currently disabled"
        )
    
    try:
        wine_recommender = WineRecommender()
        
        # Check if this is a wine recommendation request
        message_lower = chat_message.message.lower()
        wine_keywords = [
            'wein', 'wine', 'empfehlung', 'recommendation', 'schmeckt', 'taste',
            'süß', 'trocken', 'rot', 'weiß', 'rosé', 'fruchtig', 'herb'
        ]
        
        is_wine_request = any(keyword in message_lower for keyword in wine_keywords)
        
        if is_wine_request:
            # Get wine recommendations
            result = await wine_recommender.recommend_wines(chat_message.message, db)
            
            return ChatResponse(
                response=result.get("explanation", "Hier sind meine Weinempfehlungen für Sie."),
                recommendations=result.get("recommendations", []),
                context=result.get("taste_analysis", {})
            )
        else:
            # Handle general chat
            response = await _handle_general_chat(chat_message.message)
            return ChatResponse(response=response)
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )

async def _handle_general_chat(message: str) -> str:
    """
    Handle general chat messages that are not wine-related.
    """
    message_lower = message.lower()
    
    # Greetings
    if any(greeting in message_lower for greeting in ['hallo', 'hi', 'guten tag', 'servus']):
        return "Hallo! Ich bin Ihr Weinsommelier-Assistent. Beschreiben Sie mir gerne Ihren Geschmack und ich empfehle Ihnen passende Weine aus unserem Sortiment!"
    
    # Menu questions
    if any(word in message_lower for word in ['speisekarte', 'menu', 'essen', 'snacks']):
        return "Gerne! Neben unserer exquisiten Weinauswahl bieten wir auch köstliche Snacks und Getränke. Schauen Sie sich unsere Speisekarte an oder fragen Sie mich nach Weinempfehlungen!"
    
    # Location/contact
    if any(word in message_lower for word in ['adresse', 'wo', 'kontakt', 'öffnungszeiten']):
        return "Casa Vazquez befindet sich im Herzen der Stadt. Für genaue Adresse und Öffnungszeiten schauen Sie bitte in unsere Kontaktinformationen. Kann ich Ihnen bei der Weinauswahl helfen?"
    
    # Default response
    return "Das ist interessant! Ich bin spezialisiert auf Weinempfehlungen. Beschreiben Sie mir Ihren Geschmack - mögen Sie süße oder trockene Weine? Rote, weiße oder Rosé? Dann kann ich Ihnen unsere besten Weine empfehlen!"

@router.get("/chat/status")
async def get_chat_status():
    """
    Get the current status of the chatbot feature.
    """
    return {
        "enabled": settings.enable_chatbot,
        "model": settings.mcp_model_name if settings.enable_chatbot else None
    }