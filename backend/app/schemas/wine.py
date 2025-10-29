from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Dict, Any, Literal
from datetime import datetime

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
    prices: Dict[str, str] = Field(..., min_length=1)
    
    @field_validator('prices')
    @classmethod
    def validate_prices(cls, v):
        if not v:
            raise ValueError('at least one price required')
        return v

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
    prices: Optional[Dict[str, str]] = None

class Wine(WineBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str

class WineInDB(Wine):
    pass