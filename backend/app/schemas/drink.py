from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class DrinkBase(BaseModel):
    name: str
    category: str
    price: str
    volume: Optional[str] = None
    alcoholic: bool = True
    allergens: Optional[List[int]] = None
    neu: bool = False
    available: bool = True
    description: Optional[str] = None
    image: Optional[str] = None

class DrinkCreate(DrinkBase):
    pass

class DrinkUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    volume: Optional[str] = None
    alcoholic: Optional[bool] = None
    allergens: Optional[List[int]] = None
    neu: Optional[bool] = None
    available: Optional[bool] = None
    description: Optional[str] = None
    image: Optional[str] = None

class Drink(DrinkBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class DrinkInDB(Drink):
    pass