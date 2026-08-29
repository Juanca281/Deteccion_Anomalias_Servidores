<!-- INICIO_ASTAR -->

## A. Descripción del problema

Dentro del proyecto de detección de anomalías en servidores se plantea un escenario en el que, después de identificar una falla o condición anómala, es necesario determinar una ruta de menor costo hacia un servidor o recurso de recuperación.

Para representar este problema se utiliza una red de servidores conectados. Cada conexión tiene un costo que puede representar tiempo de respuesta, consumo de recursos, complejidad operativa o impacto de utilizar esa transición.

A* es pertinente porque permite combinar el costo acumulado de una ruta con una estimación del costo restante hasta la meta.

La función utilizada es:

**f(n) = g(n) + h(n)**

donde **g(n)** representa el costo acumulado y **h(n)** la estimación del costo restante.

## B. Representación del problema

- **Estado inicial:** servidor desde el cual comienza el proceso de recuperación.
- **Estados posibles:** servidores que forman parte de la infraestructura modelada.
- **Acciones u operadores:** desplazarse desde un servidor hacia otro servidor conectado.
- **Transiciones:** conexiones disponibles entre los servidores.
- **Sucesores:** servidores directamente accesibles desde el estado actual.
- **Meta:** alcanzar el Servidor-Recuperacion.
- **Costo de camino:** suma de los costos asociados a todas las conexiones utilizadas.
- **Heurística:** estimación del costo restante desde cada servidor hasta el servidor de recuperación.
- **Criterio de selección:** escoger los estados utilizando el menor valor de f(n) = g(n) + h(n).

### Estados y sucesores

- **Servidor-Web:** Servidor-App (costo 2), Servidor-Backup (costo 10)
- **Servidor-App:** Servidor-Web (costo 2), Servidor-BD (costo 2), Servidor-Monitoreo (costo 5)
- **Servidor-BD:** Servidor-App (costo 2), Servidor-Backup (costo 3)
- **Servidor-Backup:** Servidor-Web (costo 4), Servidor-BD (costo 3), Servidor-Recuperacion (costo 2)
- **Servidor-Monitoreo:** Servidor-App (costo 5), Servidor-Recuperacion (costo 2)
- **Servidor-Recuperacion:** Servidor-Backup (costo 2), Servidor-Monitoreo (costo 2)

## C. Implementación

El algoritmo A* fue implementado en `src/semana04_astar.py`.

Se utiliza una cola de prioridad para seleccionar el siguiente servidor a explorar. Para cada sucesor se calcula el nuevo costo acumulado g(n) y se suma la heurística h(n). El resultado determina la prioridad con la que el estado será explorado.

## D. Resultados y pruebas

### Caso de prueba 1

**Configuración inicial:** Servidor-Web → Servidor-Recuperacion

**Ruta obtenida:** Servidor-Web → Servidor-App → Servidor-Monitoreo → Servidor-Recuperacion

**Costo obtenido:** 9

**Estados explorados:** Servidor-Web → Servidor-App → Servidor-BD → Servidor-Monitoreo → Servidor-Backup → Servidor-Recuperacion

**Resultado esperado:** costo 9

**Comparación:** el resultado obtenido coincide con el esperado.

**Explicación:** El algoritmo debe encontrar una ruta cuyo costo total sea 9. Aunque existe una conexión directa hacia el servidor de respaldo con costo 10, existen alternativas de menor costo pasando por otros servidores.

### Caso de prueba 2

**Configuración inicial:** Servidor-App → Servidor-Recuperacion

**Ruta obtenida:** Servidor-App → Servidor-Monitoreo → Servidor-Recuperacion

**Costo obtenido:** 7

**Estados explorados:** Servidor-App → Servidor-BD → Servidor-Monitoreo → Servidor-Web → Servidor-Backup → Servidor-Recuperacion

**Resultado esperado:** costo 7

**Comparación:** el resultado obtenido coincide con el esperado.

**Explicación:** Al iniciar desde Servidor-App se reduce el costo de recuperación. A* debe encontrar una alternativa con costo total 7.

### Caso de prueba 3

**Configuración inicial:** Servidor-Web → Servidor-Recuperacion

**Modificación:** el costo entre Servidor-Monitoreo y Servidor-Recuperacion se incrementó de 2 a 10.

**Ruta obtenida:** Servidor-Web → Servidor-App → Servidor-BD → Servidor-Backup → Servidor-Recuperacion

**Costo obtenido:** 9

**Estados explorados:** Servidor-Web → Servidor-App → Servidor-BD → Servidor-Monitoreo → Servidor-Backup → Servidor-Recuperacion

**Resultado esperado:** costo 9

**Comparación:** el resultado obtenido coincide con el esperado.

**Explicación:** Se incrementa el costo entre Servidor-Monitoreo y Servidor-Recuperacion. El algoritmo debe adaptar la ruta y evitar esa conexión cuando exista una alternativa de menor costo.

## E. Análisis

### Ventajas

- A* permite considerar simultáneamente el costo recorrido y una estimación del costo pendiente.
- Puede adaptarse cuando cambian los costos de las conexiones entre servidores.
- Permite modelar decisiones de planificación posteriores a la detección de una anomalía.

### Limitaciones

- Los costos utilizados son valores definidos para la práctica y no corresponden todavía a mediciones obtenidas directamente de servidores reales.
- La calidad de A* depende de la heurística utilizada.
- Una infraestructura con gran cantidad de servidores puede aumentar el número de estados y el uso de memoria.

### Supuestos

- Se supone que las conexiones conocidas se encuentran disponibles durante cada ejecución.
- Los costos son valores positivos.
- La meta de los casos evaluados es alcanzar un servidor de recuperación.

### Posibles mejoras

- Obtener costos automáticamente a partir de métricas reales como latencia, disponibilidad o carga.
- Modificar dinámicamente la red cuando un servidor sea identificado como no disponible.
- Integrar el resultado de A* con el módulo que detecte las anomalías en etapas posteriores del proyecto.

<!-- FIN_ASTAR -->

<!-- INICIO_MINIMAX -->

## F. Minimax y juegos adversariales

### Aplicabilidad al proyecto

El proyecto de detección de anomalías en servidores no constituye directamente un problema adversarial.

Una anomalía, una sobrecarga o una falla de hardware no representan un agente racional que tome decisiones con el propósito de perjudicar al sistema.

Por esta razón, Minimax no se aplica directamente como algoritmo principal del proyecto. Para cumplir con la práctica de la Semana 04 se implementa el ejemplo de referencia mediante el juego de tres en línea.

### Diferencia entre A* y Minimax

A* corresponde a un problema de búsqueda. Explora estados utilizando costos y una heurística hasta alcanzar una meta.

Minimax corresponde a un problema adversarial. MAX intenta maximizar el resultado mientras que MIN intenta minimizarlo.

## G. Representación del problema Minimax

- **Estado:** configuración actual del tablero.
- **Acciones:** posiciones vacías disponibles.
- **Jugador MAX:** X.
- **Jugador MIN:** O.
- **Estado terminal:** victoria de X, victoria de O o empate.
- **Utilidad si gana X:** +1.
- **Utilidad si gana O:** -1.
- **Utilidad en empate:** 0.

## H. Implementación

El algoritmo se encuentra implementado en `src/semana04_minimax.py`.

Minimax genera los posibles estados sucesores del tablero de forma recursiva. Cuando juega MAX selecciona la mayor utilidad disponible y cuando juega MIN selecciona la menor.

De esta manera se supone que ambos jugadores actúan racionalmente.

## I. Resultados y casos de prueba

### Caso Minimax 1

**Escenario:** Caso 1 - Jugada ganadora

```text
X | O | X
--+---+--
O | X | 6
--+---+--
7 | 8 | O
```

**Mejor jugada:** posición 7

**Utilidad:** 1

**Nodos evaluados por Minimax:** 11

**Nodos evaluados con poda alfa-beta:** 9

**Resultado alfa-beta:** posición 7

**Explicación:** MAX puede ganar colocando X en la posición 7, completando la diagonal.

**Comparación:** Minimax y alfa-beta obtuvieron la misma decisión.

### Caso Minimax 2

**Escenario:** Caso 2 - Análisis de respuesta de MIN

```text
X | O | 3
--+---+--
4 | O | 6
--+---+--
X | 8 | 9
```

**Mejor jugada:** posición 4

**Utilidad:** 1

**Nodos evaluados por Minimax:** 136

**Nodos evaluados con poda alfa-beta:** 39

**Resultado alfa-beta:** posición 4

**Explicación:** MAX debe considerar las respuestas futuras de MIN y seleccionar la jugada que produzca la mejor utilidad posible frente a un adversario racional.

**Comparación:** Minimax y alfa-beta obtuvieron la misma decisión.

### Caso Minimax 3

**Escenario:** Caso 3 - Estado avanzado

```text
X | O | X
--+---+--
X | O | 6
--+---+--
O | X | 9
```

**Mejor jugada:** posición 6

**Utilidad:** 0

**Nodos evaluados por Minimax:** 4

**Nodos evaluados con poda alfa-beta:** 4

**Resultado alfa-beta:** posición 6

**Explicación:** El tablero tiene pocas posiciones disponibles, por lo que Minimax puede evaluar todas las alternativas restantes.

**Comparación:** Minimax y alfa-beta obtuvieron la misma decisión.

## J. Poda alfa-beta

La poda alfa-beta optimiza Minimax evitando explorar ramas que ya no pueden modificar la decisión final.

Alfa representa el mejor resultado conocido para MAX y beta representa el mejor resultado conocido para MIN.

Cuando alfa es mayor o igual que beta, una rama puede descartarse porque continuar evaluándola no cambiará la decisión final.

Esto permite reducir el número de estados evaluados manteniendo la misma decisión que Minimax.

## K. Análisis

### Ventajas

- Permite analizar decisiones frente a un adversario racional.
- Considera posibles respuestas futuras antes de decidir.
- La poda alfa-beta reduce estados innecesarios.

### Limitaciones

- El número de estados puede crecer rápidamente.
- Requiere un escenario con objetivos opuestos.
- No representa naturalmente una anomalía de servidor.

### Supuestos

- MAX y MIN actúan racionalmente.
- Ambos jugadores conocen las reglas.
- Cada jugador selecciona la decisión que más favorece su objetivo.

### Posibles mejoras

- Utilizar funciones de evaluación para árboles más grandes.
- Aplicar límites de profundidad.
- Utilizar poda alfa-beta en problemas con mayor cantidad de estados.

## Conclusión de Minimax

Minimax permitió comprender la diferencia entre un problema de búsqueda y un problema adversarial.

En el proyecto, A* se utiliza directamente para la planificación de rutas de recuperación, mientras que Minimax se desarrolla como práctica de referencia porque las anomalías de servidores no constituyen adversarios racionales.

<!-- FIN_MINIMAX -->
