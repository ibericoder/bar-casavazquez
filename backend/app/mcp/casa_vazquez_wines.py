CASA_VAZQUEZ_WINE_PROFILES = {
    'David Moreno': {
        'taste_profile': ['trocken', 'elegant', 'rund', 'würzig', 'reife beeren'],
        'characteristics': ['kirschrot', 'intensive aromen', 'barrique', 'tempranillo'],
        'recommended_for': ['elegante abende', 'fleischgerichte', 'käse'],
        'price_level': 'premium',
        'intensity': 'mittel-hoch'
    },
    'Viña Albali - Gran Reserva': {
        'taste_profile': ['trocken', 'rauchig', 'holzig', 'körperreich'],
        'characteristics': ['gran reserva', 'tempranillo', 'valdepeñas', 'barrique'],
        'recommended_for': ['besondere anlässe', 'kräftige gerichte', 'lange lagerung'],
        'price_level': 'premium',
        'intensity': 'hoch'
    },
    'Cal y Canto Tinto': {
        'taste_profile': ['weich', 'fruchtig', 'ausgewogen', 'sanfte tannine'],
        'characteristics': ['tempranillo', 'merlot', 'syrah', 'harmonisch'],
        'recommended_for': ['alltag', 'geselligkeit', 'einstieg'],
        'price_level': 'basic',
        'intensity': 'mittel'
    },
    'Marqués de Riscal': {
        'taste_profile': ['trocken', 'fruchtbetont', 'elegant', 'frisch'],
        'characteristics': ['verdejo', 'rueda', 'zitrus', 'kräuter'],
        'recommended_for': ['aperitif', 'meeresfrüchte', 'leichte speisen'],
        'price_level': 'premium',
        'intensity': 'mittel'
    },
    'Epicuro Chardonnay-Fiano': {
        'taste_profile': ['wenig säure', 'exotisch', 'würzig', 'geschmeidig'],
        'characteristics': ['chardonnay', 'fiano', 'apulien', 'tropische früchte'],
        'recommended_for': ['säureempfindliche', 'fisch', 'antipasti'],
        'price_level': 'basic',
        'intensity': 'niedrig-mittel'
    },
    'Karl Pfaffmann Grauer Burgunder': {
        'taste_profile': ['trocken', 'weich', 'dezente säure', 'fruchtig'],
        'characteristics': ['grauburgunder', 'pfalz', 'mineralisch', 'birne'],
        'recommended_for': ['deutsche küche', 'geflügel', 'mild'],
        'price_level': 'mittel',
        'intensity': 'niedrig'
    },
    'Calalenta': {
        'taste_profile': ['trocken', 'leicht', 'fruchtig', 'elegant'],
        'characteristics': ['merlot', 'abruzzen', 'hellrosa', 'feine frucht'],
        'recommended_for': ['sommer', 'leichte küche', 'aperitif'],
        'price_level': 'basic',
        'intensity': 'niedrig'
    }
}

CASA_VAZQUEZ_TASTE_KEYWORDS = {
    'trocken': {
        'keywords': ['trocken', 'dry', 'herb', 'nicht süß'],
        'recommended_wines': ['David Moreno', 'Viña Albali - Gran Reserva', 'Marqués de Riscal', 'Karl Pfaffmann Grauer Burgunder', 'Calalenta']
    },
    'fruchtig': {
        'keywords': ['fruchtig', 'fruity', 'beeren', 'früchte', 'saftig'],
        'recommended_wines': ['Cal y Canto Tinto', 'Marqués de Riscal', 'Epicuro Chardonnay-Fiano', 'Calalenta']
    },
    'elegant': {
        'keywords': ['elegant', 'fein', 'sophisticated', 'nobel', 'raffiniert'],
        'recommended_wines': ['David Moreno', 'Marqués de Riscal', 'Calalenta']
    },
    'kräftig': {
        'keywords': ['kräftig', 'stark', 'intensiv', 'vollmundig', 'körperreich'],
        'recommended_wines': ['Viña Albali - Gran Reserva', 'David Moreno']
    },
    'leicht': {
        'keywords': ['leicht', 'mild', 'zart', 'sanft', 'wenig alkohol'],
        'recommended_wines': ['Calalenta', 'Karl Pfaffmann Grauer Burgunder', 'Epicuro Chardonnay-Fiano']
    },
    'wenig_säure': {
        'keywords': ['wenig säure', 'mild', 'säurearm', 'weich', 'geschmeidig'],
        'recommended_wines': ['Epicuro Chardonnay-Fiano', 'Cal y Canto Tinto']
    },
    'besondere_anlässe': {
        'keywords': ['besonderer anlass', 'feier', 'fest', 'premium', 'exklusiv'],
        'recommended_wines': ['David Moreno', 'Viña Albali - Gran Reserva', 'Marqués de Riscal']
    }
}

CASA_VAZQUEZ_FOOD_PAIRINGS = {
    'David Moreno': ['rindfleisch', 'lamm', 'käse', 'tapas', 'chorizo'],
    'Viña Albali - Gran Reserva': ['steaks', 'wild', 'kräftiger käse', 'paella', 'jamón'],
    'Cal y Canto Tinto': ['pasta', 'pizza', 'hähnchen', 'leichte tapas', 'alltag'],
    'Marqués de Riscal': ['fisch', 'meeresfrüchte', 'salate', 'aperitif', 'gazpacho'],
    'Epicuro Chardonnay-Fiano': ['antipasti', 'leichter fisch', 'bruschetta', 'gemüse'],
    'Karl Pfaffmann Grauer Burgunder': ['geflügel', 'schweinefleisch', 'deutsche küche', 'quiche'],
    'Calalenta': ['leichte salate', 'sommer', 'frucht', 'aperitif', 'mediterran']
}

def get_casa_vazquez_wine_recommendation(wine_name: str) -> dict:
    profile = CASA_VAZQUEZ_WINE_PROFILES.get(wine_name, {})
    pairings = CASA_VAZQUEZ_FOOD_PAIRINGS.get(wine_name, [])
    
    return {
        'profile': profile,
        'food_pairings': pairings,
        'is_casa_vazquez_wine': wine_name in CASA_VAZQUEZ_WINE_PROFILES
    }

def find_wines_by_taste_casa_vazquez(taste_description: str) -> list:
    description_lower = taste_description.lower()
    recommended_wines = set()
    
    for taste_category, data in CASA_VAZQUEZ_TASTE_KEYWORDS.items():
        if any(keyword in description_lower for keyword in data['keywords']):
            recommended_wines.update(data['recommended_wines'])
    
    return list(recommended_wines)