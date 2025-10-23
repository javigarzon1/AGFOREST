export default function RouteList({routes, onSelectRoute}) {// Componente para mostrar la lista de rutas guardadas  
  return (
    <section>
        <h2>RUTAS GUARDADAS</h2>
    <ul>
      {routes.map((route) => (// Itera sobre las rutas y las muestra en una lista
        <li key={route.id}> // Usa el id guardado en la tabla de la ruta como clave única
        <strong>{route.name}</strong>
        <button onClick={() => onSelectRoute(route.id)}> Ver Ruta</button> // Botón para seleccionar la ruta
        </li>
      ))}
    </ul>
    </section>
  );
}