# 🤖 Detección de Anomalías en Servidores

Proyecto de Inteligencia Artificial enfocado en detectar automáticamente comportamientos anormales en servidores mediante el análisis de sus métricas.

## 🎯 Problema

Un servidor puede presentar comportamientos anormales antes de fallar, por ejemplo:

* CPU excesivamente alta.
* RAM casi completamente utilizada.
* Disco saturado.
* Aumento inusual de solicitudes.
* Latencia elevada.
* Incremento de errores.
* Tráfico de red fuera de lo habitual.

El sistema analizará estas variables y determinará si el comportamiento es **normal o anómalo**.

## 🧠 Ejemplo

|     CPU |     RAM |   Disco |   Latencia | Solicitudes/min | Estado          |
| ------: | ------: | ------: | ---------: | --------------: | --------------- |
|     32% |     54% |     45% |      80 ms |             120 | Normal          |
|     35% |     56% |     48% |      82 ms |             135 | Normal          |
|     31% |     55% |     47% |      78 ms |             128 | Normal          |
|     37% |     58% |     49% |      85 ms |             140 | Normal          |
| **98%** | **96%** | **91%** | **950 ms** |         **850** | 🚨 **Anomalía** |

Resultado esperado:

```text
🚨 ANOMALÍA OPERATIVA DETECTADA

CPU: 98%
RAM: 96%
Latencia: 950 ms
Solicitudes/minuto: 850

Nivel: CRÍTICO

Posible causa:
Sobrecarga del servidor.

Respuesta:
Generar alerta y recomendar revisión del servicio.
```

## 🔥 Funcionamiento

El proyecto no se limitará a reglas simples como `CPU > 90`.

El flujo será:

```text
Datos
  ↓
Limpieza y preparación
  ↓
Análisis de comportamiento normal
  ↓
Reglas de detección
  ↓
Modelo de IA para anomalías
  ↓
Clasificación
  ↓
Nivel de riesgo
  ↓
Regla de respuesta
  ↓
Alerta
```

## 🚧 Estado

**En desarrollo.**
