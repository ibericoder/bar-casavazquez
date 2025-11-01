from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from decimal import Decimal

class WineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    color: Literal['red', 'white', 'rosé']
    grape: str = Field(..., min_length=1, max_length=200)
    origin: Optional[str] = Field(None, max_length=200)
    short_description: Optional[str] = Field(None, max_length=500)
    long_description: Optional[str] = Field(None, max_length=2000)
    image: Optional[str] = Field(None, max_length=500)
    characteristics: Optional[str] = Field(None, max_length=500)
    available: bool = True
    price_bottle: Optional[Decimal] = None
    price_glass_01: Optional[Decimal] = None
    price_glass_02: Optional[Decimal] = None

class WineCreate(WineBase):
    id: str = Field(..., description="Unique wine identifier", example="w1")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "w1",
                "name": "El Coto Rioja",
                "color": "red",
                "grape": "Tempranillo",
                "origin": "Rioja, Spain",
                "short_description": "Classic Rioja with oak aging",
                "prices": {"0.1l": "4,00€", "flasche": "25,00€"},
                "available": True
            }
        }
    )

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
    price_bottle: Optional[Decimal] = None
    price_glass_01: Optional[Decimal] = None
    price_glass_02: Optional[Decimal] = None

class Wine(WineBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str

class WineInDB(Wine):
    pass