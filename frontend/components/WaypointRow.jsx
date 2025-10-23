export default function WaypointRow({ data, index, onChange, onRemove }) { // Componente para mostrar una fila de waypoint 
    return (
        <div className="wp-row">
            <input
                type="number"
                step="0.000001"
                value={data.latitude}
                onChange={(e) => onChange(index, { ...data, latitude: e.target.value })}
                placeholder="Latitud"
            />
            <input
                type="number"
                step="0.000001"
                value={data.longitude}
                onChange={(e) => onChange(index, { ...data, longitude: e.target.value })}
                placeholder="Longitud"
            />
            <button onClick={() => onRemove(index)}>Eliminar</button>
        </div>
    );
}
