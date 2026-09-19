# Semana 7 - Representaciones del reconocimiento

## Descripción

Se representó el comportamiento de un servidor mediante métodos numéricos, simbólicos y un autómata de estados. A diferencia de ingresar manualmente una secuencia, cada símbolo del autómata es generado automáticamente a partir de las telemetrías observadas.

## Datos analizados

| Lectura | CPU | RAM | Disco | Latencia | Solicitudes/min | Errores | Estado | Símbolo |
|---:|---:|---:|---:|---:|---:|---:|---|:---:|
| 1 | 45.0% | 52.0% | 61.0% | 40.0 ms | 470 | 0 | Activo | N |
| 2 | 83.0% | 74.0% | 65.0% | 90.0 ms | 720 | 2 | Activo | A |
| 3 | 94.0% | 91.0% | 94.0% | 260.0 ms | 1600 | 18 | Activo | C |
| 4 | 96.0% | 93.0% | 95.0% | 290.0 ms | 1700 | 24 | Activo | C |
| 5 | 55.0% | 61.0% | 70.0% | 62.0 ms | 530 | 1 | Activo | R |
| 6 | 48.0% | 57.0% | 68.0% | 45.0 ms | 500 | 0 | Activo | N |

## Representación numérica

| Lectura | Vector | Distancia al estado de referencia |
|---:|---|---:|
| 1 | [45.0, 52.0, 61.0, 40.0, 470.0, 0] | 0.0642 |
| 2 | [83.0, 74.0, 65.0, 90.0, 720.0, 2] | 0.4094 |
| 3 | [94.0, 91.0, 94.0, 260.0, 1600.0, 18] | 1.0234 |
| 4 | [96.0, 93.0, 95.0, 290.0, 1700.0, 24] | 1.1399 |
| 5 | [55.0, 61.0, 70.0, 62.0, 530.0, 1] | 0.1315 |
| 6 | [48.0, 57.0, 68.0, 45.0, 500.0, 0] | 0.0854 |

## Representación simbólica

| Lectura | Hechos | Conclusiones |
|---:|---|---|
| 1 | telemetrias_normales | operacion_normal |
| 2 | cpu_alta | operacion_normal |
| 3 | cpu_alta, memoria_alta, disco_critico, latencia_alta, solicitudes_altas, errores_altos | sobrecarga_recursos, posible_congestion, degradacion_servicio, riesgo_almacenamiento, anomalia_critica |
| 4 | cpu_alta, memoria_alta, disco_critico, latencia_alta, solicitudes_altas, errores_altos | sobrecarga_recursos, posible_congestion, degradacion_servicio, riesgo_almacenamiento, anomalia_critica |
| 5 | telemetrias_normales | operacion_normal |
| 6 | telemetrias_normales | operacion_normal |

## Reconocimiento mediante autómata

Secuencia generada automáticamente: `NACCRN`

| Paso | Entrada | Estado anterior | Estado resultante |
|---:|:---:|---|---|
| 1 | N | q0 - NORMAL | q0 - NORMAL |
| 2 | A | q0 - NORMAL | q1 - ADVERTENCIA |
| 3 | C | q1 - ADVERTENCIA | q3 - CRÍTICO |
| 4 | C | q3 - CRÍTICO | q3 - CRÍTICO |
| 5 | R | q3 - CRÍTICO | q4 - RECUPERACIÓN |
| 6 | N | q4 - RECUPERACIÓN | q0 - NORMAL |

**Estado final:** q0 - NORMAL.

El servidor finaliza en operación normal.

## Patrones reconocidos

- **Degradación progresiva**: El servidor evolucionó desde operación normal hacia alerta y posteriormente a un estado crítico.
- **Recuperación después de estado crítico**: Después de una condición crítica, las métricas regresaron a valores normales.
- **Recuperación completada**: Después del proceso de recuperación, el servidor regresó al estado normal.

## Comparación de representaciones

| Representación | Ventaja | Limitación | Información que se pierde |
|---|---|---|---|
| Numérica | Permite comparar métricas y medir diferencias. | Requiere interpretar los valores. | Pierde parte del significado conceptual del problema. |
| Simbólica | Facilita interpretar hechos y conclusiones. | Depende de reglas y umbrales definidos. | Reduce el detalle numérico original. |
| Autómata | Permite representar la evolución temporal del servidor. | Resume varias métricas en pocos estados. | No conserva todos los valores exactos de cada lectura. |

## Análisis

Las telemetrías se transformaron primero en representaciones numéricas y simbólicas. Posteriormente cada lectura fue clasificada automáticamente como normal, advertencia, crítica o recuperación. Estos símbolos fueron utilizados como entradas del autómata para identificar la evolución temporal del servidor y reconocer patrones de comportamiento.