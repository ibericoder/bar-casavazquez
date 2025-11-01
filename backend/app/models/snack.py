from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, DateTime, DECIMAL
from sqlalchemy.sql import func
from ..core.database import Base

class Snack(Base):
    __tablename__ = "snacks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String, nullable=False)  # 'Tapita', 'Plato', etc.
    description = Column(Text, nullable=True)
    allergens = Column(JSON, nullable=True)  # Array of allergen numbers
    vegetarian = Column(Boolean, default=False)
    vegan = Column(Boolean, default=False)
    available = Column(Boolean, default=True, nullable=False)
    image = Column(String, nullable=True)
    neu = Column(Boolean, default=False)  # New item flag
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Snack(id={self.id}, name='{self.name}', category='{self.category}')>"