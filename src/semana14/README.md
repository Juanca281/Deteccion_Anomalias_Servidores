# Semana 14 - Redes semánticas

## Proyecto

**ServidorIA - Detección de anomalías en servidores**

## Objetivo

Representar conocimiento del dominio mediante conceptos y relaciones dirigidas, interpretar oraciones simples como triples y demostrar inferencias por jerarquía y herencia.

## Conceptos del modelo

La red utiliza los siguientes conceptos principales:

1. `servidor_web`
2. `servidor_bd`
3. `servidor`
4. `activo_ti`
5. `infraestructura`
6. `monitoreo`
7. `respaldo`
8. `monitor`

## Relaciones

- `es_un`: relación jerárquica y transitiva.
- `necesita`: propiedad que el prototipo permite heredar desde categorías superiores.
- `monitorea`: relación explícita no heredable.

No se mezclan relaciones solo porque todas se representen como aristas.

## Base de conocimiento de demostración

```text
(servidor_web, es_un, servidor)
(servidor_bd, es_un, servidor)
(servidor, es_un, activo_ti)
(activo_ti, es_un, infraestructura)
(servidor, necesita, monitoreo)
(servidor_bd, necesita, respaldo)
(monitor, monitorea, servidor_web)
```

## Interpretación de oraciones

Ejemplos admitidos:

```text
El servidor_web es un servidor.
El servidor necesita monitoreo.
El monitor monitorea servidor_web.
```

El analizador normaliza minúsculas y tildes, y reconoce únicamente patrones definidos. No es un sistema de comprensión de lenguaje natural general.

## Inferencia por jerarquía

Con los hechos:

```text
servidor_web es_un servidor
servidor es_un activo_ti
activo_ti es_un infraestructura
```

el sistema puede inferir:

```text
servidor_web es_un infraestructura
```

La conclusión no se almacena como arista directa. Se obtiene recorriendo la jerarquía.

## Herencia de propiedades

Como `servidor necesita monitoreo`, `servidor_web` puede heredar la propiedad `necesita monitoreo` al pertenecer a la categoría `servidor`.

Esta herencia es una regla declarada para la práctica. No todas las relaciones del mundo real deben heredarse automáticamente.

## Consultas sin evidencia

Si se pregunta:

```text
servidor_web es_un servidor_bd
```

el resultado es `False` porque no existe una ruta jerárquica que lo demuestre. En el contexto del prototipo significa **sin evidencia suficiente en la red**, no una afirmación universal sobre toda infraestructura posible.

## Control de ciclos

Las consultas mantienen un conjunto `visitados`. Si accidentalmente aparece un ciclo en la jerarquía, un nodo ya procesado no vuelve a expandirse indefinidamente.

## Archivos

```text
semana14/
├── red_semantica.py
├── main.py
├── test_red_semantica.py
└── README.md
```

## Ejecución

```powershell
python semana14\main.py
python semana14\test_red_semantica.py
```

## Pruebas automatizadas

Las pruebas verifican:

- Relación explícita.
- Transitividad de `es_un`.
- Herencia de `necesita`.
- Consulta sin evidencia suficiente.
- Interpretación de una oración válida.
- Normalización lingüística.
- Rechazo de entradas inválidas.
- Control de ciclos.

## Limitaciones

- El parser trabaja con patrones simples.
- No interpreta negación, ambigüedad, pronombres ni frases libres.
- Solo `es_un` se considera jerárquica.
- Solo `necesita` se define como heredable.
- Las inferencias dependen totalmente de los triples registrados.

## Conclusión

La Semana 14 añade una representación gráfica y consultable del conocimiento del proyecto. La red permite diferenciar hechos explícitos de conclusiones inferidas y justificar la ruta seguida para cada respuesta.
