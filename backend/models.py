from typing import List, Optional
from pydantic import BaseModel, condecimal, Field


class WaypointCreate(BaseModel):
    order: int
    latitude: condecimal(gt=-90, lt=90, max_digits=10, decimal_places=8)  # Latitud entre -90 y 90
    longitude: condecimal(gt=-180, lt=180, max_digits=11, decimal_places=8)  # Longitud entre -180 y 180
    order: int = Field(..., ge=0)  # Índice de orden no negativo

class RouteCreate(BaseModel):
    name: str
    waypoints: List[WaypointCreate] 

class WaypointRead(BaseModel):
    id: int
    order_index: int
    latitude: float
    longitude: float

class Config:
        orm_mode = True

class RouteRead(BaseModel):
    id: int
    name: str
    created_at: Optional[str] = None
    distance_m: Optional[float] = None
    waypoints: List[WaypointRead] 

    class Config:
        orm_mode = True