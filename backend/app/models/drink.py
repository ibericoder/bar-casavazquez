from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, JSON, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class Drink(Base):
    __tablename__ = "drinks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)  # 'Cocktail', 'Softdrink', etc.
    price = Column(DECIMAL(10, 2), nullable=False)
    volume = Column(String, nullable=True)  # e.g., "0,75l"
    alcoholic = Column(Boolean, default=True, nullable=False)
    allergens = Column(JSON, nullable=True)  # Array of allergen numbers
    neu = Column(Boolean, default=False)  # New item flag
    available = Column(Boolean, default=True, nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Drink(id={self.id}, name='{self.name}', category='{self.category}')>"