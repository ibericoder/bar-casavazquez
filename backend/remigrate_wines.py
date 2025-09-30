import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models import Wine

def migrate_wines_from_files():
    """Migrate all wines from the TypeScript data files"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing wines
        session.query(Wine).delete()
        session.commit()
        print("Cleared existing wines")
        
        # Sample wines data matching the TypeScript files structure
        wines_data = [
            # RED WINES (tintos)
            {
                'id': 'r32',
                'name': 'Cal y Canto Tinto',
                'color': 'red',
                'grape': 'Tempranillo, Merlot, Syrah',
                'origin': 'Spanien',
                'short_description': 'Weich, fruchtig, ausgewogen mit sanften Tanninen.',
                'long_description': 'Cal y Canto Tinto ist eine spanische Rotwein-Cuvée aus Tempranillo, Merlot und Syrah. Im Glas zeigt er sich in tiefem Rubinrot. Das Bouquet überzeugt mit intensiven Aromen von dunklen Beeren, Kirschen und feinen Gewürznoten.',
                'prices': {'0.1l': '4,00€', '0.2l': '7,50€', 'flasche': '22,00€'},
                'characteristics': 'Trocken, weich, fruchtig, ausgewogen',
                'available': True
            },
            {
                'id': 'r29',
                'name': 'the guv`nor',
                'color': 'red',
                'grape': 'Shiraz',
                'origin': 'Australien',
                'short_description': 'Kräftiger australischer Shiraz mit intensiven Beerenfrüchten.',
                'long_description': 'Ein kraftvoller australischer Shiraz mit intensiven Aromen von dunklen Beeren und Gewürzen.',
                'prices': {'0.1l': '4,00€', '0.2l': '7,50€', 'flasche': '25,00€'},
                'characteristics': 'Trocken, kräftig, würzig',
                'available': True
            },
            {
                'id': 'r30',
                'name': 'David Moreno',
                'color': 'red',
                'grape': 'Tempranillo',
                'origin': 'Spanien',
                'short_description': 'Eleganter spanischer Tempranillo mit ausgewogener Struktur.',
                'long_description': 'Ein eleganter spanischer Tempranillo mit ausgewogener Struktur und fruchtigen Noten.',
                'prices': {'flasche': '28,00€'},
                'characteristics': 'Trocken, elegant, fruchtig',
                'available': True
            },
            {
                'id': 'r31',
                'name': 'Viña Albali - Gran Reserva',
                'color': 'red',
                'grape': 'Tempranillo',
                'origin': 'Valdepeñas, Spanien',
                'short_description': 'Traditioneller Gran Reserva mit langer Reifung.',
                'long_description': 'Ein traditioneller Gran Reserva mit langer Reifung und komplexen Aromen.',
                'prices': {'flasche': '32,00€'},
                'characteristics': 'Trocken, komplex, gereift',
                'available': True
            },
            {
                'id': 'r33',
                'name': 'Marques de Cáceres',
                'color': 'red',
                'grape': 'Tempranillo',
                'origin': 'Rioja, Spanien',
                'short_description': 'Klassischer Rioja mit traditioneller Eleganz.',
                'long_description': 'Ein klassischer Rioja mit traditioneller Eleganz und ausgewogenen Tanninen.',
                'prices': {'flasche': '35,00€'},
                'characteristics': 'Trocken, elegant, klassisch',
                'available': True
            },
            
            # WHITE WINES (blancos)
            {
                'id': 'w2',
                'name': 'Marqués de Riscal',
                'color': 'white',
                'grape': '100% Verdejo',
                'origin': 'Rueda, Spanien',
                'short_description': 'Trocken, fruchtbetonter Weißwein aus Rueda mit eleganten Kräuter- und Zitrusnoten.',
                'long_description': 'Ein erfrischender Weißwein mit lebendiger Säure und mineralischen Noten.',
                'prices': {'flasche': '34,50€'},
                'characteristics': 'Trocken, fruchtig, elegant',
                'available': True
            },
            {
                'id': 'w3',
                'name': 'Karl Pfaffmann Grauer Burgunder',
                'color': 'white',
                'grape': 'Grauer Burgunder',
                'origin': 'Deutschland',
                'short_description': 'Eleganter deutscher Grauburgunder mit feiner Frucht.',
                'long_description': 'Ein eleganter deutscher Grauburgunder mit feiner Frucht und mineralischer Note.',
                'prices': {'flasche': '26,00€'},
                'characteristics': 'Trocken, elegant, mineralisch',
                'available': True
            },
            {
                'id': 'w4',
                'name': 'Colli Vaibò Lugana',
                'color': 'white',
                'grape': 'Trebbiano di Lugana',
                'origin': 'Italien',
                'short_description': 'Italienischer Weißwein vom Gardasee.',
                'long_description': 'Ein frischer italienischer Weißwein vom Gardasee mit fruchtigen Aromen.',
                'prices': {'flasche': '28,00€'},
                'characteristics': 'Trocken, frisch, fruchtig',
                'available': True
            },
            {
                'id': 'w5',
                'name': 'Nebla Vicente Gandia Verdejo',
                'color': 'white',
                'grape': 'Verdejo',
                'origin': 'Spanien',
                'short_description': 'Spanischer Verdejo mit tropischen Fruchtaromen.',
                'long_description': 'Ein spanischer Verdejo mit tropischen Fruchtaromen und frischer Säure.',
                'prices': {'flasche': '22,00€'},
                'characteristics': 'Trocken, tropisch, frisch',
                'available': True
            },
            {
                'id': 'w6',
                'name': 'El Coto Blanco',
                'color': 'white',
                'grape': 'Viura',
                'origin': 'Rioja, Spanien',
                'short_description': 'Klassischer weißer Rioja mit floralen Noten.',
                'long_description': 'Ein klassischer weißer Rioja mit floralen Noten und ausgewogener Säure.',
                'prices': {'flasche': '24,00€'},
                'characteristics': 'Trocken, floral, ausgewogen',
                'available': True
            },
            
            # ROSÉ WINES (rosados)
            {
                'id': 'rose1',
                'name': 'Calalenta ("Kühle Nacht")',
                'color': 'rosé',
                'grape': '100% Merlot',
                'origin': 'Abruzzen, Italien',
                'short_description': 'Trocken, leichter Rosé aus Merlot-Trauben mit zartem Hellrosa und feinen Fruchtaromen.',
                'long_description': 'Ein eleganter Rosé mit subtilen Fruchtaromen und erfrischender Säure.',
                'prices': {'0.1l': '4,00€', '0.2l': '7,50€', 'flasche': '25,00€'},
                'characteristics': 'Trocken, leicht, fruchtig',
                'available': True
            },
            {
                'id': 'rose2',
                'name': 'Allure Pink Pinot Grigio (halbtrocken)',
                'color': 'rosé',
                'grape': 'Pinot Grigio',
                'origin': 'Italien',
                'short_description': 'Halbtrockener Pinot Grigio Rosé mit zarten Beerenfrüchten.',
                'long_description': 'Ein halbtrockener Pinot Grigio Rosé mit zarten Beerenfrüchten und floralen Noten.',
                'prices': {'flasche': '18,00€'},
                'characteristics': 'Halbtrocken, zart, floral',
                'available': True
            },
            {
                'id': 'rose3',
                'name': "Knipser 'Rosé 24'",
                'color': 'rosé',
                'grape': 'Spätburgunder',
                'origin': 'Deutschland',
                'short_description': 'Deutscher Spätburgunder Rosé mit feiner Eleganz.',
                'long_description': 'Ein deutscher Spätburgunder Rosé mit feiner Eleganz und fruchtiger Frische.',
                'prices': {'flasche': '32,00€'},
                'characteristics': 'Trocken, elegant, frisch',
                'available': True
            },
            {
                'id': 'rose4',
                'name': 'Rosa Dei Frati',
                'color': 'rosé',
                'grape': 'Corvina, Rondinella',
                'origin': 'Italien',
                'short_description': 'Italienischer Rosé aus dem Veneto mit delikaten Aromen.',
                'long_description': 'Ein italienischer Rosé aus dem Veneto mit delikaten Aromen und mineralischer Note.',
                'prices': {'flasche': '35,00€'},
                'characteristics': 'Trocken, delikat, mineralisch',
                'available': True
            },
            {
                'id': 'rose5',
                'name': 'Arrogant Frog',
                'color': 'rosé',
                'grape': 'Syrah, Grenache',
                'origin': 'Frankreich',
                'short_description': 'Französischer Rosé aus dem Languedoc mit intensiven Fruchtaromen.',
                'long_description': 'Ein französischer Rosé aus dem Languedoc mit intensiven Fruchtaromen und würzigen Noten.',
                'prices': {'flasche': '29,00€'},
                'characteristics': 'Trocken, intensiv, würzig',
                'available': True
            }
        ]
        
        # Insert wines
        for wine_data in wines_data:
            wine = Wine(
                id=wine_data['id'],
                name=wine_data['name'],
                color=wine_data['color'],
                grape=wine_data['grape'],
                origin=wine_data['origin'],
                short_description=wine_data['short_description'],
                long_description=wine_data['long_description'],
                prices=wine_data['prices'],
                characteristics=wine_data['characteristics'],
                available=wine_data['available'],
                image=wine_data.get('image')
            )
            session.add(wine)
        
        session.commit()
        print(f"Successfully migrated {len(wines_data)} wines")
        
        # Verify the migration
        wine_count = session.query(Wine).count()
        print(f"Total wines in database: {wine_count}")
        
        # Count by color
        colors = session.query(Wine.color, session.query(Wine).filter(Wine.color == Wine.color).count()).distinct().all()
        for color in ['red', 'white', 'rosé']:
            count = session.query(Wine).filter(Wine.color == color).count()
            print(f"{color.capitalize()}: {count} wines")
            
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    migrate_wines_from_files()