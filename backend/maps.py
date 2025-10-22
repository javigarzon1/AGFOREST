from typing import List, Optional, Annotated
from decimal import Decimal
from pydantic import BaseModel, Field

# Defino tipos anotados para latitud/longitud más compatibles con herramientas estáticas
Latitude = Annotated[Decimal, Field(gt=-90, lt=90, max_digits=10, decimal_places=8)] # Latitud válida entre -90 y 90, maximo 10 digitos y 8 decimales.
Longitude = Annotated[Decimal, Field(gt=-180, lt=180, max_digits=11, decimal_places=8)]


class WaypointCreate(BaseModel): # Modelo para crear un waypoint
    latitude: Latitude
    longitude: Longitude
    order: int = Field(..., ge=0)

class RouteCreate(BaseModel): # Modelo para crear una ruta
    name: str
    waypoints: List[WaypointCreate]

class WaypointRead(BaseModel): # Modelo para leer un waypoint
    id: int
    latitude: float
    longitude: float
    order_index: int

    class Config: # Configuración para que Pydantic pueda trabajar con ORM
        orm_mode = True

class RouteRead(BaseModel): # Modelo para leer una ruta
    id: int
    name: str
    created_at: Optional[str]
    distance_m: float
    waypoints: List[WaypointRead]

    class Config:
        orm_mode = True
