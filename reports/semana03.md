# Semana 03 - Taxonomía y clasificación

## Proyecto: Detección de anomalías en servidores

Este informe presenta la aplicación de una taxonomía de inteligencia artificial al problema de detección de anomalías operativas en servidores.

## Objetivo

Identificar qué técnicas y categorías de inteligencia artificial pueden aplicarse a diferentes situaciones relacionadas con el monitoreo y operación de servidores.

## Casos analizados

Se procesaron **20 casos**.

## Clasificación

| ID | Descripción | Categoría principal | Categorías detectadas | Técnica recomendada |
|---:|---|---|---|---|
| 1 | Detectar automaticamente cuando el uso de CPU de un servidor presenta un comportamiento anormal. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 2 | Predecir si un servidor podria presentar una falla utilizando registros historicos de CPU memoria y temperatura. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 3 | Clasificar incidentes de servidores segun su nivel de gravedad. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 4 | Determinar que servidor debe recibir primero recursos adicionales durante una situacion de sobrecarga. | Busqueda y optimizacion | Busqueda y optimizacion, Sistemas de recomendacion | Algoritmos de optimizacion para asignacion de recursos. |
| 5 | Generar una alerta cuando el consumo de memoria se encuentre fuera del comportamiento habitual. | Sistemas expertos | Sistemas expertos | Motor de reglas basado en condiciones y umbrales. |
| 6 | Identificar patrones anormales en el trafico de red de un servidor. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 7 | Recomendar acciones para reducir la carga de un servidor. | Sistemas de recomendacion | Sistemas de recomendacion | Sistema de recomendacion basado en reglas o puntuaciones. |
| 8 | Determinar si una caida en el rendimiento corresponde a una anomalia conocida. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 9 | Predecir la demanda de recursos de un servidor durante las proximas horas. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo, Busqueda y optimizacion | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 10 | Detectar incrementos inusuales en la cantidad de solicitudes recibidas por un servidor. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 11 | Analizar registros historicos para identificar patrones asociados con fallas de servidores. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 12 | Aplicar reglas para determinar cuando un servidor debe generar una alerta critica. | Sistemas expertos | Sistemas expertos | Motor de reglas basado en condiciones y umbrales. |
| 13 | Optimizar la distribucion de recursos entre varios servidores para evitar sobrecargas. | Busqueda y optimizacion | Busqueda y optimizacion | Algoritmos de optimizacion para asignacion de recursos. |
| 14 | Detectar comportamientos inusuales en el consumo de memoria de un servidor. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 15 | Clasificar el estado operativo de un servidor como normal advertencia o critico. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 16 | Predecir el tiempo aproximado antes de que un servidor pueda presentar una falla. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 17 | Determinar mediante reglas si una combinacion de CPU memoria y latencia representa una situacion de riesgo. | Sistemas expertos | Sistemas expertos | Motor de reglas basado en condiciones y umbrales. |
| 18 | Identificar desviaciones en los tiempos de respuesta de una aplicacion alojada en un servidor. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |
| 19 | Recomendar que servidor debe atender una solicitud segun su capacidad disponible. | Sistemas de recomendacion | Busqueda y optimizacion, Sistemas de recomendacion | Sistema de recomendacion basado en reglas o puntuaciones. |
| 20 | Detectar automaticamente patrones anomalos en las metricas de rendimiento de una infraestructura de servidores. | Aprendizaje automatico predictivo | Aprendizaje automatico predictivo | Isolation Forest, Random Forest, regresion o arbol de decision. |

## Distribución por categoría

- **Aprendizaje automatico predictivo:** 13 casos
- **Busqueda y optimizacion:** 2 casos
- **Sistemas expertos:** 3 casos
- **Sistemas de recomendacion:** 2 casos

## Técnicas recomendadas

### Aprendizaje automatico predictivo

Isolation Forest, Random Forest, regresion o arbol de decision.

### Sistemas expertos

Motor de reglas basado en condiciones y umbrales.

### Busqueda y optimizacion

Algoritmos de optimizacion para asignacion de recursos.

### Sistemas de recomendacion

Sistema de recomendacion basado en reglas o puntuaciones.

## Conclusión

La taxonomía permite identificar diferentes enfoques de inteligencia artificial aplicables al monitoreo de servidores. Los casos analizados muestran que la detección de anomalías puede combinar aprendizaje automático, sistemas expertos, optimización y sistemas de recomendación.

Esta clasificación constituye la base para las siguientes etapas del proyecto, donde se implementará un sistema específico para detectar anomalías en métricas de rendimiento de servidores.
