# Semana 02 - Fundamentos de Python

## Proyecto: Detección de anomalías en servidores

### Introducción

En esta semana se aplicaron los fundamentos básicos de Python al proyecto de detección de anomalías en servidores. El objetivo fue utilizar variables, tipos de datos, operadores, estructuras condicionales, funciones y estructuras de datos para representar y analizar información básica de un servidor.

### Objetivo

Aplicar los conceptos fundamentales de programación en Python a un escenario relacionado con el monitoreo de servidores, utilizando diferentes métricas para identificar su estado operativo.

### Datos utilizados

Para representar el estado de un servidor se utilizaron las siguientes métricas:

- Uso de CPU.
- Uso de memoria RAM.
- Uso de disco.
- Latencia.
- Cantidad de solicitudes por minuto.
- Cantidad de errores.
- Estado del servidor.

Estas variables permiten representar de manera básica el comportamiento de un servidor.

### Fundamentos aplicados

#### Variables y tipos de datos

Se utilizaron variables para almacenar información del servidor. Se emplearon datos de tipo `str`, `float`, `int` y `bool`.

Ejemplo:

```python
nombre_servidor = "Servidor-Web-01"
cpu = 45.5
memoria_ram = 62.0
errores = 3
servidor_activo = True