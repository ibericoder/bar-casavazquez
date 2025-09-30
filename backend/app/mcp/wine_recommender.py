from typing import List, Dict, Any, Optional
import re
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.wine import Wine
from ..core.database import get_db
from .client import MCPChatClient

class WineRecommender:
    """
    Wine recommendation engine that analyzes user taste descriptions
    and recommends wines from the Casa Vazquez collection.
    """
    
    def __init__(self):
        self.mcp_client = MCPChatClient()
        
        # Taste keywords mapping
        self.taste_keywords = {
            'süß': ['süß', 'süße', 'süßer', 'sweet', 'lieblich', 'fruchtig'],
            'trocken': ['trocken', 'trockener', 'dry', 'herb', 'crisp'],
            'vollmundig': ['vollmundig', 'kräftig', 'intensiv', 'bold', 'stark'],
            'leicht': ['leicht', 'zart', 'mild', 'light', 'sanft'],
            'fruchtig': ['fruchtig', 'fruity', 'beeren', 'kirsche', 'apfel'],
            'würzig': ['würzig', 'spicy', 'pfeffer', 'gewürz', 'scharf'],
            'blumig': ['blumig', 'floral', 'blumen', 'rose', 'veilchen'],
            'mineralisch': ['mineralisch', 'mineral', 'stein', 'schiefer']
        }
        
        # Color preferences
        self.color_keywords = {
            'rot': ['rot', 'rotwein', 'red', 'tintos'],
            'weiß': ['weiß', 'weißwein', 'white', 'blancos'],
            'rosé': ['rosé', 'rosa', 'rose', 'rosados']
        }
    
    async def recommend_wines(self, user_description: str, db: AsyncSession) -> Dict[str, Any]:
        """
        Analyze user taste description and recommend wines.
        """
        try:
            # Analyze the user description
            taste_analysis = self._analyze_taste_description(user_description)
            
            # Get wines from database
            from sqlalchemy import select
            result = await db.execute(select(Wine))
            wines = result.scalars().all()
            
            # Score and rank wines
            recommendations = self._score_wines(wines, taste_analysis)
            
            # Generate explanation using MCP client
            explanation = await self._generate_explanation(
                user_description, recommendations, taste_analysis
            )
            
            return {
                "recommendations": recommendations[:3],  # Top 3 recommendations
                "explanation": explanation,
                "taste_analysis": taste_analysis,
                "total_wines_analyzed": len(wines)
            }
            
        except Exception as e:
            return {
                "recommendations": [],
                "explanation": "Entschuldigung, bei der Weinempfehlung ist ein Fehler aufgetreten.",
                "error": str(e)
            }
    
    def _analyze_taste_description(self, description: str) -> Dict[str, Any]:
        """
        Analyze the user's taste description for keywords and preferences.
        """
        description_lower = description.lower()
        
        analysis = {
            "detected_tastes": [],
            "color_preference": None,
            "intensity_preference": None,
            "sweetness_preference": None
        }
        
        # Detect taste characteristics
        for taste, keywords in self.taste_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                analysis["detected_tastes"].append(taste)
        
        # Detect color preference
        for color, keywords in self.color_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                analysis["color_preference"] = color
                break
        
        # Determine intensity preference
        if any(word in description_lower for word in ['kräftig', 'stark', 'intensiv', 'vollmundig']):
            analysis["intensity_preference"] = "hoch"
        elif any(word in description_lower for word in ['leicht', 'zart', 'mild', 'sanft']):
            analysis["intensity_preference"] = "niedrig"
        
        # Determine sweetness preference
        if any(word in description_lower for word in ['süß', 'lieblich', 'fruchtig']):
            analysis["sweetness_preference"] = "süß"
        elif any(word in description_lower for word in ['trocken', 'herb', 'dry']):
            analysis["sweetness_preference"] = "trocken"
        
        return analysis
    
    def _score_wines(self, wines: List[Wine], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Score wines based on how well they match the taste analysis.
        """
        scored_wines = []
        
        for wine in wines:
            score = 0
            reasons = []
            
            # Color matching (highest priority)
            if analysis["color_preference"]:
                if analysis["color_preference"] == "rot" and wine.color == "red":
                    score += 50
                    reasons.append("Passende Farbe: Rotwein")
                elif analysis["color_preference"] == "weiß" and wine.color == "white":
                    score += 50
                    reasons.append("Passende Farbe: Weißwein")
                elif analysis["color_preference"] == "rosé" and wine.color == "rose":
                    score += 50
                    reasons.append("Passende Farbe: Rosé")
            
            # Taste characteristics matching
            wine_description = f"{wine.name} {wine.description}".lower()
            
            for taste in analysis["detected_tastes"]:
                if taste in wine_description or any(
                    keyword in wine_description 
                    for keyword in self.taste_keywords.get(taste, [])
                ):
                    score += 20
                    reasons.append(f"Geschmacksprofil: {taste}")
            
            # Price consideration (moderate wines often better for recommendations)
            if 15 <= wine.price <= 30:
                score += 10
                reasons.append("Gutes Preis-Leistungs-Verhältnis")
            
            scored_wines.append({
                "wine": {
                    "id": wine.id,
                    "name": wine.name,
                    "description": wine.description,
                    "price": wine.price,
                    "color": wine.color,
                    "image_url": wine.image_url
                },
                "score": score,
                "reasons": reasons
            })
        
        # Sort by score (descending)
        return sorted(scored_wines, key=lambda x: x["score"], reverse=True)
    
    async def _generate_explanation(
        self, 
        user_description: str, 
        recommendations: List[Dict[str, Any]], 
        analysis: Dict[str, Any]
    ) -> str:
        """
        Generate a personalized explanation for the recommendations.
        """
        if not recommendations:
            return "Leider konnte ich basierend auf Ihrer Beschreibung keine passenden Weine finden. Lassen Sie uns gerne nochmal sprechen!"
        
        top_wine = recommendations[0]["wine"]
        reasons = recommendations[0]["reasons"]
        
        explanation = f"Basierend auf Ihrer Beschreibung '{user_description}' empfehle ich Ihnen:\n\n"
        explanation += f"🍷 **{top_wine['name']}** ({top_wine['price']}€)\n"
        explanation += f"{top_wine['description']}\n\n"
        
        if reasons:
            explanation += "Warum dieser Wein zu Ihnen passt:\n"
            for reason in reasons[:3]:  # Top 3 reasons
                explanation += f"• {reason}\n"
        
        if len(recommendations) > 1:
            explanation += f"\nAlternativ könnte Ihnen auch unser **{recommendations[1]['wine']['name']}** gefallen."
        
        return explanation