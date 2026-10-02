# Semana 09 - Reconocimiento y procesamiento de imágenes

## Proyecto: Detección de anomalías en servidores

### 1. Imagen utilizada y relación con el proyecto

Para el desarrollo de la Semana 09 se utilizó una imagen de monitoreo de servidores correspondiente al escenario **Latencia alta**. La imagen representa gráficamente el comportamiento de diferentes métricas de telemetría utilizadas dentro del proyecto, entre ellas CPU, memoria RAM, disco, latencia, solicitudes por minuto, errores y estado del servidor.

La imagen utilizada originalmente corresponde a `prueba_latencia.png`, con una resolución de **800 x 500 píxeles**. Para cumplir con la estructura solicitada en la entrega, esta imagen debe quedar disponible también como:

`data/imagen_proyecto.png`

La relación con el proyecto consiste en utilizar técnicas de visión por computador para analizar la representación gráfica del comportamiento del servidor. Mientras que en semanas anteriores el proyecto ha trabajado directamente con valores numéricos y clasificación mediante modelos de inteligencia artificial, en esta semana se analiza la imagen resultante del monitoreo para identificar bordes, zonas segmentadas y regiones conectadas.

El procesamiento visual no reemplaza el análisis de las telemetrías numéricas. Se utiliza como una capa complementaria de evidencia e interpretación visual.

---

### 2. Resultado de Canny

Se aplicó el algoritmo de detección de bordes **Canny** sobre la imagen en escala de grises. Para la ejecución principal se utilizó:

- Sigma seleccionado: **2.0**
- Píxeles identificados como borde: **15.628**
- Porcentaje aproximado de píxeles de borde: **3,91 %**

El resultado permitió resaltar cambios de intensidad presentes en la gráfica, incluyendo líneas de las métricas, ejes, cuadrícula, texto y otras estructuras visuales.

Canny permite observar qué elementos presentan cambios suficientemente marcados dentro de la imagen. En el contexto del proyecto, esto puede servir como apoyo para identificar visualmente variaciones abruptas, picos o cambios en las curvas de monitoreo.

Sin embargo, el algoritmo no diferencia por sí mismo entre una línea correspondiente a una métrica, un eje, una leyenda o un texto. Por esta razón, los bordes detectados deben interpretarse como estructuras visuales y no directamente como anomalías del servidor.

---

### 3. Umbral Otsu obtenido

Para la segmentación automática se utilizó el método de **Otsu**, obteniendo el siguiente umbral:

- Umbral normalizado: **0.6777**
- Equivalente aproximado en escala 0-255: **172.82**

Debido a que la gráfica tiene un fondo predominantemente claro y los elementos de interés son más oscuros, se utilizó la condición:

`imagen < umbral`

en lugar de:

`imagen > umbral`

Este ajuste permite que las líneas, textos y demás elementos oscuros de la gráfica sean incluidos en la máscara binaria.

El método de Otsu permitió separar automáticamente el fondo de gran parte de las estructuras gráficas sin establecer manualmente un valor fijo de intensidad.

---

### 4. Número de regiones encontradas

Después de generar la máscara binaria mediante Otsu, se aplicó el análisis de **regiones conectadas**.

Los resultados obtenidos fueron:

- Regiones conectadas totales: **109**
- Área mínima utilizada para filtrar regiones: **50 píxeles**
- Regiones con área igual o superior a 50 píxeles: **9**

La región de mayor tamaño presentó:

- Etiqueta: **23**
- Área: **12.587 píxeles**
- Altura: **411 píxeles**
- Ancho: **719 píxeles**

El número de regiones encontradas no representa directamente el número de anomalías existentes en el servidor. Las regiones corresponden a agrupaciones de píxeles conectados que pueden pertenecer a curvas, ejes, caracteres, cuadrículas, leyendas u otros elementos de la gráfica.

La región de mayor tamaño muestra que varios elementos gráficos quedaron unidos dentro de una sola región, lo cual evidencia una de las principales limitaciones de aplicar segmentación directamente sobre una gráfica completa.

---

### 5. Cambios realizados al modificar sigma

Se realizaron pruebas con diferentes valores de sigma para observar cómo cambia la detección de bordes mediante Canny.

| Sigma | Píxeles de borde | Porcentaje |
|---:|---:|---:|
| 1.0 | 17.731 | 4,43 % |
| 2.0 | 15.628 | 3,91 % |
| 4.0 | 11.298 | 2,82 % |

Con **sigma = 1.0** se conserva una mayor cantidad de detalles y aparecen más bordes. Esto hace que se detecten líneas pequeñas, texto y otras estructuras finas.

Con **sigma = 2.0** se obtiene un resultado intermedio, razón por la cual se utilizó como valor principal dentro del análisis.

Con **sigma = 4.0** se aplica un mayor suavizado antes de detectar los bordes. Como consecuencia, se eliminan detalles pequeños y disminuye la cantidad de píxeles detectados como borde.

Entre sigma 1.0 y sigma 4.0, la cantidad de píxeles de borde disminuyó aproximadamente un **36,3 %**.

Esto demuestra que sigma influye directamente en el nivel de detalle que conserva Canny. Un sigma bajo conserva más información visual, mientras que un sigma alto reduce ruido y detalles pequeños.

---

### 6. Limitaciones encontradas

Durante el procesamiento se identificaron varias limitaciones.

La primera limitación es que la imagen contiene elementos que no corresponden directamente a las métricas del servidor, como títulos, números, ejes, cuadrículas y leyendas. Tanto Canny como Otsu pueden interpretar estos elementos como información relevante.

La segunda limitación es que una región conectada no equivale necesariamente a una anomalía. Una misma región puede agrupar diferentes líneas de la gráfica y otros componentes visuales.

La tercera limitación es que al convertir la gráfica a escala de grises se pierde información asociada a los colores originales. Esto dificulta diferenciar visualmente qué curva corresponde a CPU, RAM, disco, latencia u otra métrica.

Otra limitación es que una gráfica es solamente una representación visual de datos que originalmente ya existen en formato numérico. Por esta razón, utilizar visión artificial como único mecanismo de detección de anomalías sería menos preciso que analizar directamente las telemetrías.

En consecuencia, el procesamiento de imágenes se considera dentro del proyecto como una herramienta complementaria de análisis visual y generación de evidencia.

---

### 7. Aplicación futura dentro del proyecto

El procesamiento desarrollado durante la Semana 09 puede utilizarse como una capa adicional dentro del sistema de detección de anomalías en servidores.

La arquitectura conceptual puede plantearse de la siguiente manera:

`Telemetrías numéricas → Detección de anomalía → Generación de gráfica → Procesamiento visual → Evidencia e interpretación`

Los datos numéricos continuarían siendo la fuente principal para determinar si el servidor presenta comportamiento normal, advertencia, anomalía, estado crítico o recuperación.

Posteriormente, la gráfica generada podría analizarse mediante visión artificial para producir evidencia visual adicional. Canny puede ayudar a identificar cambios bruscos y estructuras presentes en las curvas, Otsu permite separar regiones visuales automáticamente y el análisis de regiones conectadas permite estudiar agrupaciones presentes dentro de la imagen.

Como mejora futura se propone trabajar solamente sobre la zona útil de la gráfica, excluyendo títulos, leyendas, números y ejes. Esto permitiría reducir regiones que no están relacionadas directamente con las métricas del servidor.

También podría combinarse el procesamiento de Semana 09 con el modelo neuronal desarrollado durante la Semana 08. De esta forma, la red neuronal podría realizar la clasificación general de la imagen y las técnicas de visión por computador podrían aportar evidencia visual para explicar qué estructuras fueron detectadas.

Por lo tanto, la Semana 09 amplía el proyecto desde el análisis exclusivamente numérico y neuronal hacia un enfoque multimodal en el que las telemetrías y sus representaciones gráficas pueden analizarse de forma complementaria.

---

## Evidencias generadas

Durante el desarrollo se generaron las siguientes evidencias:

- `src/semana09_vision.py`
- `artifacts/semana09_vision.png`
- `artifacts/semana09_comparacion_sigma.png`
- `artifacts/semana09_regiones.png`
- `src/semana09_comparar_sigma.py`
- `src/semana09_analizar_regiones.py`
- `src/semana09_analisis.py`
- `data/imagen_proyecto.png`
- `reports/semana09.md`

El archivo principal requerido por la guía es `src/semana09_vision.py` y la evidencia visual principal corresponde a `artifacts/semana09_vision.png`. Los demás archivos fueron desarrollados como ampliación para comparar parámetros, analizar regiones e integrar el procesamiento con el frontend del proyecto.
