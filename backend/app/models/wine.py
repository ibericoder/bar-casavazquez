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
    
    price_bottle = Column(DECIMAL(10, 2), nullable=True)
    price_glass_01 = Column(DECIMAL(10, 2), nullable=True)
    price_glass_02 = Column(DECIMAL(10, 2), nullable=True)
    
    def __repr__(self):
        return f"<Wine(id='{self.id}', name='{self.name}', color='{self.color}')>"