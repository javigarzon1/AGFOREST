from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
import math

from . import models, schemas
from .database import engine, Base, get_db


Base.metadata.create_all(bind=engine)
app = FastAPI(" AGFOREST API ") 
# Fórmula de Haversine para calcular la distancia entre dos puntos geográficos pasando la latitud y la longitud como parámetros
def haversine_meters(lat1, lon1, lat2, lon2):
    R = 6371000  
    phi1 = math.radians(lat1) # Convertir grados a radianes
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1) # Diferencia de latitud en radianes
    delta_lambda = math.radians(lon2 - lon1) # Diferencia de longitud en radianes

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2 # Componente 'a' de la fórmula de Haversine
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))# Ángulo central
    return R * c # Distancia en metros

def compute_route_distance(waypoints): # Calcular la distancia total de una ruta dada una lista de waypoints
    if not waypoints or len(waypoints) < 2:
        return 0.0
    total = 0.0
    for i in range(len(waypoints) - 1): # Iterar sobre cada par de waypoints consecutivos
        total += haversine_meters(
            waypoints[i].latitude,# latitud del waypoint actual
            waypoints[i].longitude, # longitud del waypoint actual
            waypoints[i + 1].latitude,  # latitud del siguiente waypoint
            waypoints[i + 1].longitude  # longitud del siguiente waypoint
        )
    return total # Distancia total en metros

@app.post("/routes/", response_model=schemas.RouteRead) # Endpoint para crear una nueva ruta con waypoints
def create_route(payload: schemas.RouteCreate, db: Session = Depends(get_db)):
    if not payload.waypoints or len(payload.waypoints) == 0:
        raise HTTPException(status_code=400, detail="Al menos un waypoint es requerido para crear una ruta.")   
  
    route = models.Route(name=payload.name) # Crear una nueva instancia de Route con el nombre proporcionado 
    db.add(route)
    db.flush() # Asignar un ID a la ruta antes de agregar los waypoints
    
    wp_objs = []
    sorted_wps = sorted(payload.waypoints, key=lambda wp: wp.order) # Ordenar los waypoints por su atributo 'order'
    for idx, wp in enumerate(sorted_wps):
        wp_obj = models.Waypoint(  # Crear una nueva instancia de Waypoint
            route_id=route.id, # ID de la ruta a la que pertenece el waypoint
            order=wp.order, # orden del waypoint
            latitude=wp.latitude, # latitud del waypoint
            longitude=wp.longitude,  # longitud del waypoint
            order_index=wp.order  # índice de orden para mantener la secuencia de waypoints
        )
        db.add(wp_obj)
        wp_objs.append(wp_obj)
    db.commit() # Guardar los cambios en la base de datos
    db.refresh(route) # Refrescar la instancia de ruta para obtener los datos actualizados
    for w in wp_objs:
        db.refresh(w) # Refrescar cada instancia de waypoint
    
    distance = compute_route_distance(wp_objs) #
    # si el modelo Route soporta un campo de distance, intentar actualizarlo
    try:
        route.distance = float(distance)
        db.add(route)
        db.commit()
        db.refresh(route)
    except Exception:
        pass

    return route
    response = schemas.RouteRead(
        id=route.id,
        name=route.name,
        created_at=route.created_at.isoformat() if route.created_at else None,
        distance_m=distance,
        waypoints=[schemas.WaypointRead(
            id=w.id,
            order_index=w.order_inde,
            latitude=float(w.latitude),
            longitude=float(w.longitude)
        ) for w in route.waypoints
]
    )
    return response

@app.get("/routes/", response_model=List[schemas.RouteRead]) # Endpoint para listar todas las rutas almacenadas en la base de datos
def list_routes(db: Session = Depends(get_db)):
    routes = db.query(models.Route).order_by(models.Route.created_at.desc().all()) # Consultar todas las rutas en la base de datos
    results = []
    for route in routes:
        distance = compute_route_distance(route.waypoints) # Calcular la distancia de la ruta
        route.distance = float(distance) #
        id=route.id,
        name=route.name,
        created_at=route.created_at.isoformat() if route.created_at else None, # Formatear la fecha de creación como una cadena ISO
        distance_m=distance,
        waypoints=[schemas.WaypointRead( #
            id=w.id,
            order_index=w.order_index,
            latitude=float(w.latitude),
            longitude=float(w.longitude)
        ) for w in route.waypoints]
        results.append(route) # Agregar la ruta a la lista de resultados
    return results

@app.get("/routes/{route_id}", response_model=schemas.RouteRead) # Endpoint para obtener los detalles de una ruta específica por su ID
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first() # Consultar la ruta por su ID
    if not route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada.") # Manejar el caso en que la ruta no existe
    distance = compute_route_distance(route.waypoints) # Calcular la distancia de la ruta
    return schemas.RouteRead(# Construir la respuesta con los detalles de la ruta 
        id=route.id,
        name=route.name,
        created_at=route.created_at.isoformat() if route.created_at else None, 
        distance_m=distance,
        waypoints=[schemas.WaypointRead(
            id=w.id,
            order_index=w.order_index,
            latitude=float(w.latitude),
            longitude=float(w.longitude)
        ) for w in route.waypoints]
    )
    route.distance = float(distance)
    db.add(route)
    db.commit()
    db.refresh(route)
    response = schemas.RouteRead( # Construir la respuesta con los detalles de la ruta
        id=route.id,
        name=route.name,
        created_at=route.created_at.isoformat() if route.created_at else None,
        distance_m=distance,
        waypoints=[schemas.WaypointRead(
            id=w.id,
            order_index=w.order_index,
            latitude=float(w.latitude),
            longitude=float(w.longitude)
        ) for w in route.waypoints]
    )
    return response