# Semana 8 – Representaciones del reconocimiento

## Detección de anomalías en servidores mediante imágenes, redes neuronales, SQLite y ontologías

### 1. Introducción

Durante la Semana 8 se desarrolló una nueva etapa del proyecto acumulativo **Detección de Anomalías en Servidores**, enfocada en las representaciones utilizadas para el reconocimiento de patrones mediante imágenes.

El objetivo principal consistió en complementar los análisis numéricos y simbólicos desarrollados durante las semanas anteriores con un sistema capaz de recibir una gráfica de monitoreo de un servidor, procesarla mediante una red neuronal artificial, identificar el posible estado representado en la imagen, almacenar la evidencia del análisis en una base de datos y posteriormente interpretar el resultado mediante una ontología.

De esta manera, el flujo desarrollado durante la semana quedó compuesto por tres elementos principales:

1. Reconocimiento mediante una red neuronal.
2. Registro de evidencia utilizando SQLite.
3. Representación semántica mediante una ontología.

Este enfoque corresponde al flujo conceptual trabajado durante la Semana 8, donde una imagen es procesada por un modelo de reconocimiento, posteriormente registrada como evidencia y finalmente asociada con conceptos que permiten interpretar su significado dentro de un dominio específico.

---

## 2. Objetivo general

Implementar un sistema de reconocimiento de imágenes orientado al monitoreo de servidores que permita clasificar gráficas de telemetría mediante una red neuronal MLP, almacenar los resultados obtenidos en una base de datos SQLite e interpretar las predicciones mediante una ontología adaptada al dominio de soporte e infraestructura tecnológica.

---

## 3. Objetivos específicos

- Crear un conjunto de imágenes representativas de diferentes estados de funcionamiento de un servidor.

- Entrenar una red neuronal artificial para reconocer patrones presentes en gráficas de monitoreo.

- Clasificar las imágenes en cinco estados relacionados con anomalías de infraestructura.

- Evaluar el rendimiento del modelo mediante métricas de clasificación y una matriz de confusión.

- Probar el modelo con imágenes que no formen parte directamente del entrenamiento.

- Registrar las predicciones realizadas como evidencia utilizando una base de datos SQLite.

- Crear una ontología que represente conceptos y relaciones asociadas al monitoreo de servidores.

- Integrar la red neuronal, la base de datos y la ontología dentro de un único flujo de análisis.

- Integrar el funcionamiento de Semana 8 dentro del frontend acumulativo del proyecto.

---

# 4. Clases utilizadas para el reconocimiento

Para adaptar la práctica al proyecto de detección de anomalías en servidores se definieron cinco categorías.

| Clase | Descripción |
|---|---|
| Normal | El servidor presenta valores estables de CPU, RAM, disco y latencia. |
| Sobrecarga CPU/RAM | La utilización de CPU y memoria RAM presenta valores elevados. |
| Latencia alta | El servidor presenta tiempos de respuesta elevados mientras las demás métricas permanecen relativamente normales. |
| Saturación de disco | El porcentaje de utilización del almacenamiento se encuentra próximo a su capacidad máxima. |
| Estado crítico | Varias métricas presentan simultáneamente valores elevados o críticos. |

Estas clases permiten relacionar el reconocimiento visual directamente con el objetivo general del proyecto acumulativo.

---

# 5. Construcción del dataset

Inicialmente se desarrolló un script encargado de generar automáticamente gráficas de monitoreo utilizando las siguientes métricas:

- Uso de CPU.
- Uso de memoria RAM.
- Uso de disco.
- Latencia.

Cada gráfica representa el comportamiento de un servidor durante varios intervalos de tiempo.

El dataset definitivo quedó conformado por:

| Categoría | Cantidad de imágenes |
|---|---:|
| Normal | 200 |
| Sobrecarga CPU/RAM | 200 |
| Latencia alta | 200 |
| Saturación de disco | 200 |
| Estado crítico | 200 |
| **Total** | **1.000** |

La distribución se mantuvo balanceada para evitar que alguna categoría tuviera una representación considerablemente superior a las demás durante el entrenamiento.

Las imágenes generadas mantuvieron una estructura visual relativamente estandarizada. Esta decisión se tomó después de realizar una primera prueba con una gran cantidad de variaciones visuales que redujo significativamente la capacidad del modelo para distinguir correctamente las métricas.

La variación definitiva se concentró principalmente en los datos representados:

- Promedios de CPU.
- Promedios de RAM.
- Utilización del disco.
- Latencia.
- Ruido en las señales.
- Picos de utilización.
- Tendencias positivas o negativas.

De esta manera, el modelo debía aprender principalmente las diferencias entre los estados de las métricas y no los cambios de diseño de las gráficas.

---

# 6. Preprocesamiento de las imágenes

Antes de enviar cada imagen al modelo se aplicó un proceso de transformación.

Cada imagen fue:

1. Cargada desde el dataset.
2. Convertida a escala de grises.
3. Redimensionada a una resolución de **64 × 64 píxeles**.
4. Convertida en un arreglo numérico.
5. Normalizada en un rango entre 0 y 1.
6. Transformada en un vector de una sola dimensión.

La resolución utilizada genera:

**64 × 64 = 4.096 características por imagen.**

La transformación convierte cada gráfica en una representación numérica compatible con la red neuronal.

El material de Semana 8 utiliza el mismo principio al convertir imágenes en vectores numéricos que posteriormente son procesados por una red neuronal.

---

# 7. División del dataset

El dataset de 1.000 imágenes se dividió utilizando la siguiente proporción:

- **75 % para entrenamiento.**
- **25 % para prueba.**

Por lo tanto:

| Conjunto | Imágenes |
|---|---:|
| Entrenamiento | 750 |
| Prueba | 250 |

La separación se realizó utilizando `train_test_split` y estratificación por clase para conservar una cantidad proporcional de ejemplos de cada categoría.

El uso de una división entre entrenamiento y prueba permite evaluar el comportamiento del modelo con información que no participó directamente en el ajuste de sus parámetros.

---

# 8. Arquitectura de la red neuronal

Para realizar el reconocimiento se utilizó la clase:

`MLPClassifier`

de la biblioteca `scikit-learn`.

La arquitectura implementada fue:

```text
Entrada
4096 características
        ↓
Capa oculta
128 neuronas
        ↓
Capa oculta
64 neuronas
        ↓
Salida
5 clases
```

La función de activación utilizada fue `ReLU` y el algoritmo de optimización fue `Adam`.

También se utilizó `early_stopping` con el objetivo de detener el entrenamiento cuando el modelo dejara de presentar mejoras durante varias iteraciones.

El modelo finalmente fue almacenado utilizando `pickle` en:

```text
artifacts/modelo_mlp.pkl
```

Además se creó:

```text
artifacts/modelo_config.json
```

donde se almacenan parámetros relacionados con la configuración del modelo, resolución de las imágenes, clases y resultados del entrenamiento.

El almacenamiento del modelo entrenado permite posteriormente realizar nuevas predicciones sin tener que repetir el entrenamiento con las 1.000 imágenes.

---

# 9. Resultados del entrenamiento

El modelo final obtuvo:

**Accuracy: 98,80 %**

Sobre un conjunto de prueba compuesto por 250 imágenes.

Los resultados obtenidos fueron:

| Clase | Precision | Recall | F1-score | Imágenes |
|---|---:|---:|---:|---:|
| Normal | 1.00 | 0.96 | 0.98 | 50 |
| Sobrecarga CPU/RAM | 0.98 | 1.00 | 0.99 | 50 |
| Latencia alta | 0.96 | 0.98 | 0.97 | 50 |
| Saturación de disco | 1.00 | 1.00 | 1.00 | 50 |
| Estado crítico | 1.00 | 1.00 | 1.00 | 50 |

La matriz de confusión obtenida fue:

```text
[[48  0  2  0  0]
 [ 0 50  0  0  0]
 [ 0  1 49  0  0]
 [ 0  0  0 50  0]
 [ 0  0  0  0 50]]
```

De las 250 imágenes utilizadas para prueba, únicamente tres fueron clasificadas incorrectamente.

Dos imágenes correspondientes a la clase Normal fueron clasificadas como Latencia alta y una imagen de Latencia alta fue clasificada como Sobrecarga CPU/RAM.

Las clases Saturación de disco y Estado crítico obtuvieron una clasificación correcta en las 50 imágenes utilizadas para cada categoría.

Aunque el accuracy constituye una métrica importante, este valor debe analizarse junto con otras métricas como precisión, recall, F1-score y matriz de confusión. El material de la Semana 8 también destaca que el accuracy debe interpretarse con cautela y no utilizarse como única evidencia sobre el desempeño del modelo.

---

# 10. Problema encontrado durante el desarrollo

Durante una primera versión del dataset se intentó introducir una gran cantidad de variaciones visuales en las gráficas.

Entre las modificaciones se encontraban:

- Diferentes tamaños.
- Diferentes resoluciones.
- Posiciones variables de la leyenda.
- Diferentes estilos de línea.
- Marcadores.
- Cambios en la escala.
- Diferentes títulos.

El modelo entrenado utilizando estas imágenes obtuvo un accuracy aproximado de:

**72,80 %**

El principal problema se presentó en la categoría Saturación de disco, donde el modelo no realizó ninguna predicción correcta para esta clase.

La matriz de confusión permitió detectar que las imágenes de saturación de disco estaban siendo confundidas principalmente con estados normales, sobrecarga y latencia.

Después del análisis se concluyó que la cantidad de variaciones visuales dificultaba el reconocimiento mediante el MLP, debido a que el modelo trabaja directamente con la distribución de los píxeles.

Como solución se estandarizó nuevamente la apariencia de las gráficas y se mantuvieron las variaciones principalmente sobre los valores de las métricas.

Después de esta modificación el accuracy aumentó desde aproximadamente:

```text
72,80 %
```

hasta:

```text
98,80 %
```

Este resultado permitió comprobar la importancia de realizar correctamente el proceso de representación y preparación de los datos antes de entrenar un modelo.

---

# 11. Prueba con una imagen externa

Después del entrenamiento se creó una imagen adicional de prueba que no pertenecía al conjunto utilizado durante el entrenamiento.

La imagen simulaba un escenario de:

**Latencia alta**

En una primera versión del modelo se obtuvo:

```text
Predicción: Latencia alta
Confianza: 22,65 %
```

Aunque la clasificación fue correcta, la distribución de probabilidades indicaba que el modelo tenía una alta incertidumbre.

Después de mejorar el dataset y aumentar la resolución a 64 × 64, la misma prueba obtuvo:

```text
Predicción: Latencia alta
Confianza: 49,04 %
```

Las probabilidades fueron:

| Clase | Probabilidad |
|---|---:|
| Latencia alta | 49,04 % |
| Sobrecarga CPU/RAM | 31,61 % |
| Saturación de disco | 9,11 % |
| Normal | 8,46 % |
| Estado crítico | 1,79 % |

La predicción nuevamente fue correcta y presentó una separación mayor respecto a las demás clases.

Sin embargo, este resultado permitió establecer una limitación importante: el modelo funciona mejor con imágenes cuya estructura se encuentra dentro del formato utilizado durante el entrenamiento.

---

# 12. Clasificación del nivel de confianza

Para evitar presentar una predicción como completamente segura cuando la probabilidad obtenida es baja, se definieron tres niveles.

| Confianza | Interpretación |
|---|---|
| Mayor o igual a 55 % | Confiable |
| Entre 40 % y 54,99 % | Moderada |
| Menor a 40 % | No concluyente |

Por ejemplo, la imagen utilizada para probar latencia alta obtuvo:

```text
Predicción: Latencia alta
Confianza: 49,04 %
Nivel: Moderada
```

Esta clasificación permite complementar el resultado del modelo con una interpretación más comprensible para el usuario.

---

# 13. Registro de evidencia mediante SQLite

Después de obtener la predicción se implementó una base de datos SQLite denominada:

```text
artifacts/imagenes.db
```

Su objetivo es conservar evidencia de cada imagen analizada.

La tabla principal almacena información relacionada con:

- Identificador de evidencia.
- Nombre de la imagen.
- Ruta de la imagen.
- Identificador de la clase.
- Predicción realizada.
- Porcentaje de confianza.
- Nivel de confianza.
- Probabilidades por clase.
- Fecha del análisis.

El sistema permite posteriormente consultar el historial de predicciones realizadas.

El uso de SQLite representa la segunda capa del flujo de Semana 8, donde el reconocimiento generado por la red neuronal se transforma en evidencia persistente. Este enfoque corresponde al concepto de utilizar una base de datos para almacenar metadatos y evidencia asociados al reconocimiento.

---

# 14. Ontología del dominio

Como tercera capa del sistema se desarrolló una ontología orientada al monitoreo de servidores utilizando la biblioteca:

```text
NetworkX
```

La ontología fue almacenada utilizando el formato:

```text
GraphML
```

en:

```text
artifacts/ontologia.graphml
```

Entre los conceptos principales incluidos se encuentran:

- Servidor.
- Gráfica de monitoreo.
- Métrica.
- CPU.
- RAM.
- Disco.
- Latencia.
- Anomalía.
- Estado.
- Estado normal.
- Sobrecarga CPU/RAM.
- Latencia alta.
- Saturación de disco.
- Estado crítico.
- Predicción.
- Evidencia.

También se definieron relaciones como:

```text
Servidor
    --genera-->
GraficaMonitoreo
```

```text
GraficaMonitoreo
    --representa-->
Metrica
```

```text
SobrecargaCPURAM
    --afecta-->
CPU
```

```text
SobrecargaCPURAM
    --afecta-->
RAM
```

```text
LatenciaAlta
    --afecta-->
Latencia
```

```text
SaturacionDisco
    --afecta-->
Disco
```

```text
Prediccion
    --se_registra_como-->
Evidencia
```

Esto permite representar no solamente el resultado de la red neuronal, sino también su significado dentro del dominio tecnológico.

La actividad de Semana 8 solicita precisamente adaptar la ontología al proyecto acumulativo utilizando conceptos y relaciones propias del dominio.

---

# 15. Interpretación ontológica

Una vez obtenida la predicción, el sistema consulta la representación conceptual correspondiente.

Por ejemplo:

```text
Predicción:
Latencia alta
```

se transforma en:

```text
Concepto:
LatenciaAlta

Tipo:
Anomalia

Métrica afectada:
Latencia
```

La interpretación generada es:

> Se identifica un incremento anormal en la latencia del servidor, lo cual puede afectar los tiempos de respuesta.

Otro ejemplo corresponde a:

```text
Predicción:
Sobrecarga CPU/RAM
```

que se relaciona con:

```text
Concepto:
SobrecargaCPURAM

Métricas afectadas:
CPU
RAM
```

La ontología permite pasar de una clasificación matemática a una representación con significado dentro del proyecto.

---

# 16. Integración de los componentes

Posteriormente se desarrolló un script encargado de unificar todos los componentes implementados durante la semana.

El flujo final quedó definido de la siguiente manera:

```text
Imagen
   ↓
Preprocesamiento
64 × 64
   ↓
Red neuronal MLP
   ↓
Predicción
   ↓
Confianza
   ↓
SQLite
   ↓
Registro de evidencia
   ↓
Ontología
   ↓
Interpretación semántica
```

El script integrado permite ejecutar todo el proceso utilizando una sola imagen como entrada.

El resultado contiene:

- Nombre de la imagen.
- Clase predicha.
- Porcentaje de confianza.
- Nivel de confianza.
- Probabilidades por clase.
- ID de evidencia SQLite.
- Fecha del análisis.
- Concepto ontológico.
- Tipo de concepto.
- Métricas afectadas.
- Interpretación del resultado.

Este flujo representa la integración de reconocimiento, evidencia y significado planteada conceptualmente durante la Semana 8.

---

# 17. Integración con Flask

Para integrar Semana 8 con el aplicativo acumulativo se creó un nuevo endpoint:

```text
POST /api/semana8
```

El endpoint permite recibir una imagen desde el frontend mediante una solicitud `multipart/form-data`.

El backend realiza las siguientes operaciones:

```text
Frontend
   ↓
Carga de imagen
   ↓
Flask
   ↓
Validación del archivo
   ↓
Almacenamiento temporal
   ↓
semana08_analisis.py
   ↓
modelo_mlp.pkl
   ↓
imagenes.db
   ↓
ontologia.graphml
   ↓
JSON
   ↓
Frontend
```

Los formatos permitidos son:

- PNG.
- JPG.
- JPEG.

También se utiliza `secure_filename` para controlar el nombre del archivo y se genera un identificador único para evitar conflictos entre imágenes con el mismo nombre.

---

# 18. Integración con el frontend

Se creó una nueva sección denominada:

**Semana 8 – Reconocimiento neuronal y ontología**

La interfaz permite al usuario:

1. Seleccionar una gráfica.
2. Visualizar una vista previa.
3. Ejecutar el análisis.
4. Consultar la predicción.
5. Visualizar el porcentaje de confianza.
6. Consultar todas las probabilidades.
7. Visualizar el ID de evidencia almacenado en SQLite.
8. Consultar el concepto ontológico.
9. Visualizar las métricas afectadas.
10. Consultar la interpretación semántica.

La interfaz mantiene la misma línea visual utilizada en las semanas anteriores del proyecto acumulativo.

---

# 19. Imágenes adicionales de prueba

Para facilitar las pruebas del sistema se desarrolló un script capaz de generar cinco imágenes independientes.

Las imágenes representan:

```text
prueba_normal.png
prueba_sobrecarga.png
prueba_latencia.png
prueba_disco.png
prueba_critico.png
```

Estas imágenes permiten evaluar cada una de las cinco categorías de manera independiente desde el frontend o mediante el script de análisis.

Estas imágenes no forman parte de las 1.000 utilizadas originalmente para construir el dataset principal.

---

# 20. Artefactos generados

Durante Semana 8 se generaron los siguientes artefactos principales:

```text
artifacts/
├── modelo_mlp.pkl
├── modelo_config.json
├── imagenes.db
└── ontologia.graphml
```

### modelo_mlp.pkl

Contiene el modelo neuronal entrenado.

### modelo_config.json

Contiene información sobre:

- Resolución de entrada.
- Número de características.
- Capas ocultas.
- Clases.
- Accuracy.
- Cantidad de imágenes de entrenamiento.
- Cantidad de imágenes de prueba.

### imagenes.db

Almacena las evidencias generadas durante los análisis.

### ontologia.graphml

Representa los conceptos y relaciones semánticas utilizadas para interpretar las predicciones.

La generación de estos artefactos corresponde con los entregables técnicos planteados en la práctica de Semana 8.

---

# 21. Archivos principales desarrollados

Los principales scripts incorporados durante esta semana fueron:

```text
src/
├── semana08_generar_dataset.py
├── semana08_entrenar_modelo.py
├── semana08_predecir_imagen.py
├── semana08_generar_prueba.py
├── semana08_evidencia.py
├── semana08_ontologia.py
└── semana08_analisis.py
```

### semana08_generar_dataset.py

Genera las 1.000 imágenes utilizadas para entrenar el modelo.

### semana08_entrenar_modelo.py

Carga el dataset, realiza el preprocesamiento, divide los datos, entrena el MLP, evalúa sus resultados y almacena el modelo.

### semana08_predecir_imagen.py

Permite utilizar el modelo entrenado para clasificar una imagen nueva.

### semana08_generar_prueba.py

Genera cinco imágenes adicionales utilizadas para validar las diferentes categorías.

### semana08_evidencia.py

Administra el almacenamiento y consulta de evidencia utilizando SQLite.

### semana08_ontologia.py

Construye la ontología y realiza la interpretación semántica de las predicciones.

### semana08_analisis.py

Integra el reconocimiento neuronal, SQLite y la ontología dentro de un único flujo.

---

# 22. Limitaciones

El modelo desarrollado corresponde a un prototipo académico y presenta algunas limitaciones importantes.

La principal limitación consiste en que el dataset fue generado sintéticamente utilizando una estructura de gráfica determinada.

Por esta razón, una gráfica obtenida desde un sistema externo puede presentar:

- Diferentes escalas.
- Diferentes colores.
- Diferentes resoluciones.
- Diferente distribución.
- Otras etiquetas.
- Otras posiciones de leyenda.
- Distintos tipos de visualización.

Estas diferencias pueden reducir considerablemente la confianza del modelo.

Por lo tanto, el accuracy de 98,80 % debe interpretarse específicamente sobre imágenes generadas bajo una distribución similar a la utilizada durante el entrenamiento y no como evidencia de que el modelo puede reconocer cualquier gráfica de monitoreo existente.

Otra limitación consiste en que se utiliza una red neuronal MLP sobre los píxeles aplanados de la imagen. Para aplicaciones más avanzadas podría utilizarse una red neuronal convolucional, debido a que este tipo de arquitectura está diseñada específicamente para trabajar con información visual.

---

# 23. Posibles mejoras futuras

Como continuación del proyecto podrían implementarse las siguientes mejoras:

- Utilizar imágenes provenientes de herramientas reales de monitoreo.

- Incorporar nuevas variaciones controladas al dataset.

- Entrenar una red neuronal convolucional.

- Incrementar la cantidad de imágenes por categoría.

- Añadir nuevas anomalías.

- Incorporar métricas adicionales como solicitudes por minuto y cantidad de errores.

- Relacionar la información visual de Semana 8 con las telemetrías numéricas trabajadas en Semana 7.

- Utilizar el historial almacenado en SQLite para generar estadísticas.

- Visualizar gráficamente la ontología desde el frontend.

- Permitir comparar diferentes análisis históricos.

---

# 24. Relación con las semanas anteriores

Semana 8 complementa directamente el trabajo desarrollado durante las semanas anteriores.

Mientras Semana 7 trabaja principalmente con telemetrías numéricas y secuencias temporales como:

```text
CPU
RAM
Disco
Latencia
Solicitudes
Errores
Estado del servidor
```

Semana 8 transforma parte de esta información en una representación visual.

La diferencia principal puede resumirse como:

```text
SEMANA 7
Datos numéricos y secuencias
        ↓
Clasificación de estados
        ↓
Representación simbólica
```

```text
SEMANA 8
Imagen de monitoreo
        ↓
Red neuronal
        ↓
Predicción
        ↓
Evidencia
        ↓
Ontología
```

Por lo tanto, Semana 8 no reemplaza los desarrollos anteriores, sino que agrega una nueva representación del conocimiento dentro del proyecto acumulativo.

---

# 25. Conclusiones

Durante la Semana 8 se logró implementar satisfactoriamente un sistema de reconocimiento de patrones aplicado al monitoreo de servidores.

El modelo neuronal definitivo fue entrenado utilizando un dataset compuesto por 1.000 imágenes distribuidas entre cinco categorías y obtuvo un accuracy de **98,80 %** sobre un conjunto de prueba de 250 imágenes.

El proceso de desarrollo permitió comprobar que la calidad y consistencia de la representación de los datos tiene una influencia considerable sobre el desempeño del modelo. Una primera versión con variaciones visuales excesivas obtuvo solamente 72,80 % de accuracy y presentó dificultades importantes para reconocer la saturación de disco. Después de reorganizar el dataset, el desempeño aumentó considerablemente.

También se comprobó que un accuracy elevado dentro del dataset no garantiza la misma confianza al utilizar imágenes externas. La prueba de latencia alta permitió evidenciar esta diferencia al obtener una predicción correcta con una confianza de 49,04 %.

Además del reconocimiento neuronal, se implementó una base de datos SQLite para conservar evidencia de las predicciones realizadas y una ontología en formato GraphML para representar el significado de cada anomalía dentro del dominio del monitoreo de servidores.

Finalmente, los tres componentes fueron integrados dentro de un único flujo y posteriormente conectados con Flask y el frontend del proyecto acumulativo.

De esta manera, Semana 8 permitió integrar tres conceptos fundamentales:

```text
RECONOCIMIENTO
      +
EVIDENCIA
      +
SIGNIFICADO
```

El resultado amplía las capacidades del proyecto de detección de anomalías y demuestra cómo diferentes técnicas de inteligencia artificial y representación del conocimiento pueden trabajar conjuntamente dentro de una misma aplicación.