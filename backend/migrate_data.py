import sys
import os
import json
from pathlib import Path

# Add the backend and project root to the Python path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models import Wine

def get_sample_wines():
    """Sample wine data for testing"""
    return [
        {
            'id': 'w1',
            'name': 'Cal y Canto Tinto',
            'color': 'red',
            'grape': 'Tempranillo, Merlot, Syrah',
            'origin': 'Spanien',
            'shortDescription': 'Weich, fruchtig, ausgewogen mit sanften Tanninen.',
            'longDescription': 'Ein harmonischer Rotwein mit weichen Tanninen und fruchtigen Aromen.',
            'prices': {
                '0.1l': '4,00€',
                '0.2l': '7,50€',
                'flasche': '22,00€'
            },
            'characteristics': 'Weich, fruchtig, ausgewogen',
            'available': True,
            'image': None
        },
        {
            'id': 'w2',
            'name': 'Marqués de Riscal',
            'color': 'white',
            'grape': '100% Verdejo',
            'origin': 'Rueda, Spanien',
            'shortDescription': 'Trocken, fruchtbetonter Weißwein aus Rueda mit eleganten Kräuter- und Zitrusnoten.',
            'longDescription': 'Ein erfrischender Weißwein mit lebendiger Säure und mineralischen Noten.',
            'prices': {
                'flasche': '34,50€'
            },
            'characteristics': 'Trocken, fruchtig, elegant',
            'available': True,
            'image': None
        },
        {
            'id': 'w3',
            'name': 'Calalenta ("Kühle Nacht")',
            'color': 'rosé',
            'grape': '100% Merlot',
            'origin': 'Abruzzen, Italien',
            'shortDescription': 'Trocken, leichter Rosé aus Merlot-Trauben mit zartem Hellrosa und feinen Fruchtaromen.',
            'longDescription': 'Ein eleganter Rosé mit subtilen Fruchtaromen und erfrischender Säure.',
            'prices': {
                '0.1l': '4,00€',
                '0.2l': '7,50€',
                'flasche': '25,00€'
            },
            'characteristics': 'Trocken, leicht, fruchtig',
            'available': True,
            'image': None
        }
    ]

# Use sample data instead of trying to import TypeScript
existing_vinos = get_sample_wines()

def migrate_wines():
    """Migrate existing wine data to the database"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing data
        session.query(Wine).delete()
        
        # Migrate wines
        for wine_data in existing_vinos:
            wine = Wine(
                id=str(wine_data['id']),
                name=wine_data['name'],
                color=wine_data['color'],
                grape=wine_data['grape'],
                origin=wine_data.get('origin'),
                short_description=wine_data.get('shortDescription'),
                long_description=wine_data.get('longDescription'),
                image=wine_data.get('image'),
                characteristics=wine_data.get('characteristics'),
                available=wine_data.get('available', True),
                prices=wine_data['prices']
            )
            session.add(wine)
        
        session.commit()
        print(f"Successfully migrated {len(existing_vinos)} wines to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error migrating wines: {e}")
    finally:
        session.close()

def migrate_sample_drinks():
    """Add some sample drinks to the database"""
    from app.models import Drink
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    sample_drinks = [
        {
            "name": "Wasser Classic/Naturell",
            "volume": "0,75l",
            "price": "6,9€",
            "category": "Softdrink",
            "alcoholic": False,
            "allergens": []
        },
        {
            "name": "Yuzu Sour",
            "price": "10,5€",
            "category": "Cocktail",
            "alcoholic": True,
            "allergens": [11]
        },
        {
            "name": "Espresso Martini",
            "price": "10,5€",
            "category": "Cocktail",
            "alcoholic": True,
            "allergens": [8, 13]
        },
        {
            "name": "Negroni",
            "price": "10,5€",
            "category": "Cocktail",
            "alcoholic": True,
            "allergens": [4]
        },
        {
            "name": "Gin Tonic",
            "price": "7,9€",
            "category": "Cocktail",
            "alcoholic": True,
            "allergens": [24]
        }
    ]
    
    try:
        # Clear existing drinks
        session.query(Drink).delete()
        
        for drink_data in sample_drinks:
            drink = Drink(**drink_data)
            session.add(drink)
        
        session.commit()
        print(f"Successfully added {len(sample_drinks)} sample drinks to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error adding sample drinks: {e}")
    finally:
        session.close()

def migrate_sample_snacks():
    """Add some sample snacks to the database"""
    from app.models import Snack
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    sample_snacks = [
        {
            "name": "Aceitunas mixtas",
            "price": "4,5€",
            "category": "Tapita",
            "description": "Gemischte Oliven mit Kräutern",
            "vegetarian": True,
            "vegan": True,
            "allergens": []
        },
        {
            "name": "Jamón Ibérico",
            "price": "16,0€",
            "category": "Plato",
            "description": "Premium iberischer Schinken",
            "vegetarian": False,
            "vegan": False,
            "allergens": []
        },
        {
            "name": "Tortilla Española",
            "price": "8,5€",
            "category": "Plato",
            "description": "Traditionelles spanisches Kartoffelomelett",
            "vegetarian": True,
            "vegan": False,
            "allergens": [11]
        }
    ]
    
    try:
        # Clear existing snacks
        session.query(Snack).delete()
        
        for snack_data in sample_snacks:
            snack = Snack(**snack_data)
            session.add(snack)
        
        session.commit()
        print(f"Successfully added {len(sample_snacks)} sample snacks to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error adding sample snacks: {e}")
    finally:
        session.close()

def migrate_sample_notifications():
    """Add some sample notifications to the database"""
    from app.models import Notification
    from datetime import datetime, timedelta
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    sample_notifications = [
        {
            "title": "Happy Hour",
            "message": "Mo-Fr bis 19 Uhr zu jeder Flasche Rosé eine Plato Mixto aufs Haus.",
            "type": "info",
            "active": True,
            "priority": 1,
            "target_page": "wine"
        },
        {
            "title": "Saludos desde Madrid",
            "message": "Diesen Samstag bekommt ihr zu jedem Getränk eine kleine Tapita, ganz wie ihr es aus der Hauptstadt Spaniens kennt.",
            "type": "success",
            "active": True,
            "priority": 2,
            "target_page": "all",
            "expires_at": datetime.utcnow() + timedelta(days=7)
        }
    ]
    
    try:
        # Clear existing notifications
        session.query(Notification).delete()
        
        for notification_data in sample_notifications:
            notification = Notification(**notification_data)
            session.add(notification)
        
        session.commit()
        print(f"Successfully added {len(sample_notifications)} sample notifications to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error adding sample notifications: {e}")
    finally:
        session.close()

def main():
    print("Starting data migration...")
    migrate_wines()
    migrate_sample_drinks()
    migrate_sample_snacks()
    migrate_sample_notifications()
    print("Data migration completed!")

if __name__ == "__main__":
    main()