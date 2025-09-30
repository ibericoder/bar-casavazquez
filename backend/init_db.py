import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from app.core.database import Base, engine
from app.core.config import settings
from app.models import Wine, Drink, Snack, Notification

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def main():
    create_tables()

if __name__ == "__main__":
    main()