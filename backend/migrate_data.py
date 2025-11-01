import sys
import os
import json
from pathlib import Path
from decimal import Decimal
import re

# Add the backend and project root to the Python path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

def parse_price(price_str):
    """Convert German price format to Decimal: '3,9€' -> 3.9 or '€39,50' -> 39.50"""
    if not price_str:
        return Decimal('0')
    price_clean = re.sub(r'[€\s]', '', str(price_str))
    price_clean = price_clean.replace(',', '.')
    try:
        return Decimal(price_clean)
    except:
        return Decimal('0')

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models import Wine, User, UserRole
from app.core.auth import get_password_hash

def load_json_data(filename):
    """Load data from JSON file"""
    data_file = backend_dir / 'data' / filename
    if not data_file.exists():
        print(f"Warning: {filename} not found, using empty list")
        return []
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load wine data from JSON
existing_vinos = load_json_data('wines.json')

def migrate_wines():
    """Migrate existing wine data to the database"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing data
        session.query(Wine).delete()
        
        # Migrate wines
        for wine_data in existing_vinos:
            prices = wine_data.get('prices', {})
            wine = Wine(
                id=str(wine_data['id']),
                name=wine_data['name'],
                color=wine_data['color'],
                grape=wine_data['grape'],
                origin=wine_data.get('origin'),
                short_description=wine_data.get('short_description'),
                long_description=wine_data.get('long_description'),
                image=wine_data.get('image'),
                characteristics=wine_data.get('characteristics'),
                available=wine_data.get('available', True),
                price_bottle=parse_price(prices.get('flasche')),
                price_glass_01=parse_price(prices.get('0.1l')),
                price_glass_02=parse_price(prices.get('0.2l'))
            )
            session.add(wine)
        
        session.commit()
        print(f"Successfully migrated {len(existing_vinos)} wines to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error migrating wines: {e}")
    finally:
        session.close()

def migrate_drinks():
    """Migrate drinks from JSON to database"""
    from app.models import Drink
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    drinks_data = load_json_data('drinks.json')
    
    try:
        # Clear existing drinks
        session.query(Drink).delete()
        
        for drink_data in drinks_data:
            drink_data['price'] = parse_price(drink_data.get('price', '0'))
            drink = Drink(**drink_data)
            session.add(drink)
        
        session.commit()
        print(f"Successfully migrated {len(drinks_data)} drinks to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error migrating drinks: {e}")
    finally:
        session.close()

def migrate_snacks():
    """Migrate snacks from JSON to database"""
    from app.models import Snack
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    snacks_data = load_json_data('snacks.json')
    
    try:
        # Clear existing snacks
        session.query(Snack).delete()
        
        for snack_data in snacks_data:
            snack_data['price'] = parse_price(snack_data.get('price', '0'))
            snack = Snack(**snack_data)
            session.add(snack)
        
        session.commit()
        print(f"Successfully migrated {len(snacks_data)} snacks to the database")
        
    except Exception as e:
        session.rollback()
        print(f"Error migrating snacks: {e}")
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

def create_default_admin():
    """Create a default admin user"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if admin user already exists
        existing_admin = session.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@casavazquez.com",
            hashed_password=get_password_hash("admin"),  # Simple password for now
            full_name="Casa Vazquez Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        session.add(admin_user)
        session.commit()
        print("Created default admin user (username: admin, password: admin123)")
        print("⚠️  IMPORTANT: Change the admin password after first login!")
        
    except Exception as e:
        session.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        session.close()

def main():
    print("Starting data migration...")
    create_default_admin()
    migrate_wines()
    migrate_drinks()
    migrate_snacks()
    migrate_sample_notifications()
    print("Data migration completed!")

if __name__ == "__main__":
    main()