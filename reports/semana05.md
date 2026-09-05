# Semana 05 - Sistema híbrido

## Proyecto: Detección de anomalías en servidores

El sistema combina reglas expertas, recuperación de información con TF-IDF y similitud coseno, clasificación de texto y procesamiento básico de lenguaje natural.

## Configuración

- Entradas en la base de conocimiento: 8
- Reglas expertas: 5
- Ejemplos etiquetados: 15
- Categorías: almacenamiento, disponibilidad, red, rendimiento, seguridad

## Pruebas

| # | Consulta | Regla activada | Evidencia recuperada | Similitud | Clasificación |
|---|---|---|---|---:|---|
| 1 | El servidor de aplicaciones está muy lento y presenta consumo alto de CPU y memoria. | R1 - revisar_rendimiento | CPU alta o memoria elevada pueden causar lentitud en el servidor. Se recomienda revisar procesos activos y consumo de recursos antes de reiniciar servicios. | 0.436 | rendimiento |
| 2 | El servidor web no resuelve nombres DNS y presenta pérdida de conectividad. | R2 - revisar_conectividad | Errores DNS o pérdida de conectividad deben revisarse validando resolución de nombres, puerta de enlace, enlace de red y comunicación con otros servidores. | 0.372 | red |
| 3 | El servidor de base de datos tiene el disco casi lleno y no puede guardar registros. | R3 - revisar_almacenamiento | Si el disco tiene poco espacio disponible, se deben revisar archivos temporales, logs y crecimiento de bases de datos antes de liberar almacenamiento. | 0.426 | almacenamiento |

## Explicación de resultados

### Consulta 1

**Entrada:** El servidor de aplicaciones está muy lento y presenta consumo alto de CPU y memoria.

- **R1 - revisar_rendimiento:** se activó por las palabras `cpu, memoria, lento`. Acción: Revisar consumo de CPU, memoria y procesos activos.

- **Evidencia recuperada:** CPU alta o memoria elevada pueden causar lentitud en el servidor. Se recomienda revisar procesos activos y consumo de recursos antes de reiniciar servicios.
- **Similitud:** 0.436
- **Clasificación:** rendimiento

### Consulta 2

**Entrada:** El servidor web no resuelve nombres DNS y presenta pérdida de conectividad.

- **R2 - revisar_conectividad:** se activó por las palabras `dns, conectividad`. Acción: Validar DNS, enlace de red, puerta de enlace y comunicación entre servidores.

- **Evidencia recuperada:** Errores DNS o pérdida de conectividad deben revisarse validando resolución de nombres, puerta de enlace, enlace de red y comunicación con otros servidores.
- **Similitud:** 0.372
- **Clasificación:** red

### Consulta 3

**Entrada:** El servidor de base de datos tiene el disco casi lleno y no puede guardar registros.

- **R3 - revisar_almacenamiento:** se activó por las palabras `disco, registros`. Acción: Revisar uso de disco, crecimiento de logs y espacio disponible.

- **Evidencia recuperada:** Si el disco tiene poco espacio disponible, se deben revisar archivos temporales, logs y crecimiento de bases de datos antes de liberar almacenamiento.
- **Similitud:** 0.426
- **Clasificación:** almacenamiento

## Relación con los temas de la Semana 5

- **Sistema experto:** las reglas representan decisiones explicables del dominio.
- **Ingeniería del conocimiento:** la experiencia del dominio se organiza en la base de conocimiento, reglas y ejemplos etiquetados.
- **Recuperación de información:** TF-IDF y similitud coseno buscan la evidencia textual más relacionada con la consulta.
- **Reconocimiento de patrones:** el clasificador identifica patrones de palabras y asigna una categoría.
- **PLN:** las consultas en lenguaje natural se normalizan y se transforman en señales que pueden procesar las reglas y los modelos.

## Limitaciones

- La base de conocimiento es pequeña y debe crecer con casos reales.
- Las reglas dependen de palabras clave y pueden no cubrir todas las formas de expresar un incidente.
- El clasificador utiliza pocos ejemplos de entrenamiento, por lo que puede equivocarse con consultas muy diferentes.
- La similitud textual no reemplaza la validación técnica de un administrador de servidores.

## Conclusión

La Semana 5 agrega al proyecto un sistema híbrido sencillo y trazable. Cada consulta deja evidencia de la regla aplicada, el documento recuperado, la similitud obtenida y la categoría predicha.
