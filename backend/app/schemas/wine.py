from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class WineBase(BaseModel):
    name: str
    color: str  # 'red', 'white', 'rosé'
    grape: str
    origin: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    image: Optional[str] = None
    characteristics: Optional[str] = None
    available: bool = True
    prices: Dict[str, str]  # e.g., {"0.1l": "4,00€", "flasche": "25,00€"}

class WineCreate(WineBase):
    id: str

class WineUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    grape: Optional[str] = None
    origin: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    image: Optional[str] = None
    characteristics: Optional[str] = None
    available: Optional[bool] = None
    prices: Optional[Dict[str, str]] = None

class Wine(WineBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str

class WineInDB(Wine):
    pass