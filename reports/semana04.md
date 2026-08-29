# Semana 04 - Búsqueda y toma de decisiones

## Proyecto: Detección de anomalías en servidores

Durante la Semana 04 se aplican algoritmos clásicos de inteligencia artificial relacionados con búsqueda, heurísticas y toma de decisiones.

Los ejercicios se adaptan al proyecto de detección de anomalías en servidores con el propósito de integrar los conceptos vistos en clase con un escenario de infraestructura tecnológica.

---

## 1. Búsqueda A*

El algoritmo A* se utiliza para encontrar una ruta de menor costo entre servidores dentro de una red.

### Componentes del problema

- **Estado inicial:** Servidor-Web
- **Meta:** Servidor-Recuperacion
- **Acción:** desplazarse desde un servidor hacia otro servidor conectado.
- **Costo:** valor asociado a cada transición entre servidores.
- **Heurística:** estimación del costo restante hasta alcanzar el servidor objetivo.

### Resultado

**Ruta encontrada:** Servidor-Web → Servidor-App → Servidor-Monitoreo → Servidor-Recuperacion

**Costo total:** 9

### Relación con el proyecto

Dentro del sistema de detección de anomalías, A* puede representar un mecanismo de planificación para buscar una ruta alternativa de atención o recuperación cuando uno de los servidores presenta una falla.

<!-- FIN_ASTAR -->

---

## 2. Minimax

Minimax se utiliza como mecanismo de toma de decisiones después de detectar una anomalía en un servidor.

### Estado

El servidor principal presenta una anomalía operativa y el sistema debe seleccionar una acción.

### Acciones disponibles

- Mantener servidor activo
- Redistribuir carga
- Activar servidor de respaldo

### Función de utilidad

- **Mantener servidor activo:** utilidad 2
- **Redistribuir carga:** utilidad 6
- **Activar servidor de respaldo:** utilidad 8

### Resultado

**Mejor acción:** Activar servidor de respaldo

**Utilidad obtenida:** 8

### Relación con el proyecto

Minimax puede utilizarse como componente de decisión después de detectar una anomalía. El sistema puede comparar diferentes acciones y seleccionar aquella que represente una mejor respuesta para mantener la disponibilidad de los servicios.

## Conclusión de la Semana 04

A* y Minimax representan dos capacidades diferentes dentro de un sistema inteligente. A* permite buscar rutas considerando costos y una heurística, mientras que Minimax permite analizar alternativas de decisión mediante una función de utilidad.

Dentro del proyecto, ambos algoritmos pueden complementar el proceso de detección de anomalías: A* como mecanismo de planificación y Minimax como mecanismo de selección de una respuesta.

<!-- FIN_MINIMAX -->