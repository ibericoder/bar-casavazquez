from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base

class Wine(Base):
    __tablename__ = "wines"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    color = Column(String, nullable=False)  # 'red', 'white', 'rosé'
    grape = Column(String, nullable=False)
    origin = Column(String, nullable=True)
    short_description = Column(Text, nullable=True)
    long_description = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    characteristics = Column(String, nullable=True)
    available = Column(Boolean, default=True, nullable=False)
    
    # Prices stored as JSON for flexibility
    # Example: {"0.1l": "4,00€", "0.2l": "7,50€", "flasche": "25,00€"}
    prices = Column(JSON, nullable=False)
    
    def __repr__(self):
        return f"<Wine(id='{self.id}', name='{self.name}', color='{self.color}')>"