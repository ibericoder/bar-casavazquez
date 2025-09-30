from typing import List, Dict, Any, Optional
import re
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.wine import Wine
from ..core.database import get_db
from .client import MCPChatClient
from .casa_vazquez_wines import (
    CASA_VAZQUEZ_WINE_PROFILES, 
    CASA_VAZQUEZ_TASTE_KEYWORDS,
    CASA_VAZQUEZ_FOOD_PAIRINGS,
    get_casa_vazquez_wine_recommendation,
    find_wines_by_taste_casa_vazquez
)

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
        Enhanced with Casa Vazquez specific knowledge.
        """
        description_lower = description.lower()
        
        analysis = {
            "detected_tastes": [],
            "color_preference": None,
            "intensity_preference": None,
            "sweetness_preference": None,
            "original_description": description  # Store for Casa Vazquez matching
        }
        
        # Detect taste characteristics using Casa Vazquez keywords
        for taste_category, data in CASA_VAZQUEZ_TASTE_KEYWORDS.items():
            if any(keyword in description_lower for keyword in data['keywords']):
                analysis["detected_tastes"].append(taste_category)
        
        # Also check generic taste keywords
        for taste, keywords in self.taste_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                if taste not in analysis["detected_tastes"]:
                    analysis["detected_tastes"].append(taste)
        
        # Detect color preference
        for color, keywords in self.color_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                analysis["color_preference"] = color
                break
        
        # Determine intensity preference
        if any(word in description_lower for word in ['kräftig', 'stark', 'intensiv', 'vollmundig', 'körperreich']):
            analysis["intensity_preference"] = "hoch"
        elif any(word in description_lower for word in ['leicht', 'zart', 'mild', 'sanft', 'wenig alkohol']):
            analysis["intensity_preference"] = "niedrig"
        
        # Determine sweetness preference
        if any(word in description_lower for word in ['süß', 'lieblich', 'fruchtig']):
            analysis["sweetness_preference"] = "süß"
        elif any(word in description_lower for word in ['trocken', 'herb', 'dry', 'nicht süß']):
            analysis["sweetness_preference"] = "trocken"
        
        return analysis
    
    def _score_wines(self, wines: List[Wine], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Score wines based on how well they match the taste analysis.
        Enhanced with Casa Vazquez specific wine knowledge.
        """
        scored_wines = []
        
        # Get Casa Vazquez specific recommendations first
        casa_vazquez_recommendations = find_wines_by_taste_casa_vazquez(analysis.get('original_description', ''))
        
        for wine in wines:
            score = 0
            reasons = []
            
            # Casa Vazquez specific wine knowledge boost (highest priority)
            if wine.name in casa_vazquez_recommendations:
                score += 60
                cv_info = get_casa_vazquez_wine_recommendation(wine.name)
                if cv_info['is_casa_vazquez_wine']:
                    reasons.append("Perfekt für Ihren Geschmack - Casa Vazquez Empfehlung")
            
            # Color matching (high priority)
            if analysis["color_preference"]:
                if analysis["color_preference"] == "rot" and wine.color == "red":
                    score += 40
                    reasons.append("Passende Farbe: Rotwein")
                elif analysis["color_preference"] == "weiß" and wine.color == "white":
                    score += 40
                    reasons.append("Passende Farbe: Weißwein")
                elif analysis["color_preference"] == "rosé" and wine.color == "rose":
                    score += 40
                    reasons.append("Passende Farbe: Rosé")
            
            # Casa Vazquez specific taste profile matching
            wine_description = f"{wine.name} {wine.short_description or ''} {wine.characteristics or ''}".lower()
            
            # Check against Casa Vazquez wine profiles
            if wine.name in CASA_VAZQUEZ_WINE_PROFILES:
                cv_profile = CASA_VAZQUEZ_WINE_PROFILES[wine.name]
                
                # Match taste preferences
                for detected_taste in analysis["detected_tastes"]:
                    if detected_taste in cv_profile.get('taste_profile', []):
                        score += 25
                        reasons.append(f"Casa Vazquez Geschmacksprofil: {detected_taste}")
                
                # Intensity matching
                if analysis.get("intensity_preference"):
                    wine_intensity = cv_profile.get('intensity', '').lower()
                    if analysis["intensity_preference"] == "hoch" and ("hoch" in wine_intensity or "stark" in wine_intensity):
                        score += 20
                        reasons.append("Passende Intensität: kräftig")
                    elif analysis["intensity_preference"] == "niedrig" and ("niedrig" in wine_intensity or "leicht" in wine_intensity):
                        score += 20
                        reasons.append("Passende Intensität: mild")
                
                # Sweetness matching  
                if analysis.get("sweetness_preference") == "trocken" and "trocken" in cv_profile.get('taste_profile', []):
                    score += 20
                    reasons.append("Trocken wie gewünscht")
            
            # Generic taste characteristics matching (fallback)
            for taste in analysis["detected_tastes"]:
                if taste in wine_description or any(
                    keyword in wine_description 
                    for keyword in self.taste_keywords.get(taste, [])
                ):
                    score += 15
                    reasons.append(f"Geschmacksprofil: {taste}")
            
            # Price consideration (moderate wines often better for recommendations)
            wine_price = self._extract_bottle_price(wine.prices)
            if wine_price and 20 <= wine_price <= 35:
                score += 10
                reasons.append("Gutes Preis-Leistungs-Verhältnis")
            
            scored_wines.append({
                "wine": {
                    "id": wine.id,
                    "name": wine.name,
                    "description": wine.short_description or wine.long_description,
                    "price": wine_price,
                    "color": wine.color,
                    "grape": wine.grape,
                    "origin": wine.origin,
                    "characteristics": wine.characteristics,
                    "image_url": wine.image
                },
                "score": score,
                "reasons": reasons,
                "casa_vazquez_recommendation": wine.name in casa_vazquez_recommendations
            })
        
        # Sort by score (descending)
        return sorted(scored_wines, key=lambda x: x["score"], reverse=True)
    
    def _extract_bottle_price(self, prices: dict) -> Optional[float]:
        """Extract bottle price from prices JSON"""
        if not prices:
            return None
        
        bottle_price_str = prices.get('flasche', '')
        if bottle_price_str:
            # Extract number from string like "25,00€" or "€29,50"
            import re
            price_match = re.search(r'(\d+(?:,\d{2})?)', bottle_price_str)
            if price_match:
                price_str = price_match.group(1).replace(',', '.')
                try:
                    return float(price_str)
                except ValueError:
                    pass
        return None
    
    async def _generate_explanation(
        self, 
        user_description: str, 
        recommendations: List[Dict[str, Any]], 
        analysis: Dict[str, Any]
    ) -> str:
        """
        Generate a personalized explanation for the recommendations.
        Enhanced with Casa Vazquez specific wine knowledge.
        """
        if not recommendations:
            return "Leider konnte ich basierend auf Ihrer Beschreibung keine passenden Weine finden. Lassen Sie uns gerne nochmal sprechen!"
        
        top_wine = recommendations[0]["wine"]
        reasons = recommendations[0]["reasons"]
        is_cv_recommendation = recommendations[0].get("casa_vazquez_recommendation", False)
        
        explanation = f"Basierend auf Ihrer Beschreibung '{user_description}' empfehle ich Ihnen:\n\n"
        explanation += f"🍷 **{top_wine['name']}** "
        
        # Add price information
        if top_wine.get('price'):
            explanation += f"({top_wine['price']}€ Flasche)\n"
        else:
            explanation += "\n"
        
        # Add Casa Vazquez specific information
        if is_cv_recommendation and top_wine['name'] in CASA_VAZQUEZ_WINE_PROFILES:
            cv_profile = CASA_VAZQUEZ_WINE_PROFILES[top_wine['name']]
            explanation += f"*{top_wine['grape']} aus {top_wine['origin']}*\n\n"
            explanation += f"{top_wine['description']}\n\n"
            
            # Add food pairing suggestions
            if top_wine['name'] in CASA_VAZQUEZ_FOOD_PAIRINGS:
                pairings = CASA_VAZQUEZ_FOOD_PAIRINGS[top_wine['name']][:3]  # Top 3 pairings
                explanation += f"**Perfekt zu:** {', '.join(pairings)}\n\n"
        else:
            explanation += f"{top_wine['description']}\n\n"
        
        if reasons:
            explanation += "**Warum dieser Wein zu Ihnen passt:**\n"
            for reason in reasons[:3]:  # Top 3 reasons
                explanation += f"• {reason}\n"
        
        # Add alternative suggestions
        if len(recommendations) > 1:
            alt_wine = recommendations[1]['wine']
            explanation += f"\n**Alternative:** {alt_wine['name']}"
            if alt_wine.get('price'):
                explanation += f" ({alt_wine['price']}€)"
            
            if recommendations[1].get("casa_vazquez_recommendation"):
                explanation += " - auch eine Casa Vazquez Spezialität!"
        
        # Add a personal sommelier touch
        if is_cv_recommendation:
            explanation += f"\n\n*Als Ihr Casa Vazquez Sommelier kann ich Ihnen versichern: Dieser Wein wird Ihnen gefallen! 🍷*"
        
        return explanation