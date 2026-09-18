# Semana 07 - Representaciones del reconocimiento

## Proyecto: Detección de anomalías en servidores

La Semana 07 representa un mismo evento de monitoreo mediante tres enfoques diferentes: representación numérica, representación simbólica y reconocimiento mediante autómatas.

## Datos analizados

- **Temperatura:** 75.0 °C
- **Carga:** 0.88
- **Errores:** 4
- **Secuencia temporal:** AAAN

---

## 1. Representación numérica

El servidor se representa mediante un vector formado por temperatura, carga y cantidad de errores.

**Vector actual:** [75.0, 0.88, 4.0]

**Vector de referencia:** [70.0, 0.8, 2.0]

**Vector normalizado actual:** [0.75, 0.88, 0.4]

**Distancia numérica:** 0.221

Una distancia pequeña indica que el estado actual es parecido al estado de referencia. Una distancia mayor indica una diferencia más significativa.

---

## 2. Representación simbólica

Los valores numéricos se convierten en conceptos que pueden ser utilizados por reglas explícitas.

**Hechos detectados:** carga_alta, errores_presentes, temperatura_alta

**Conclusiones simbólicas:** riesgo_termico, degradacion_servicio, anomalia_critica

Por ejemplo, cuando temperatura_alta y carga_alta están presentes, el sistema puede concluir riesgo_termico.

---

## 3. Reconocimiento mediante autómata

El autómata analiza una secuencia temporal de estados del servidor.

- **N:** comportamiento normal.
- **A:** comportamiento anómalo.

El estado q2 representa la detección de dos o más anomalías consecutivas al final de la secuencia.

**Secuencia:** AAAN

**Estado final:** q0

**¿Se reconoce una anomalía persistente?:** No

### Recorrido

- q0 --A--> q1
- q1 --A--> q2
- q2 --A--> q2
- q2 --N--> q0

---

## Comparación de representaciones

| Representación | Ventaja | Limitación | Pérdida de información |
|---|---|---|---|
| Numérica | Permite medir diferencias y comparar estados mediante distancias. | Requiere definir escalas y valores de referencia. | No explica por sí sola el significado operativo del resultado. |
| Simbólica | Produce hechos y conclusiones fáciles de explicar. | Depende de umbrales y reglas definidas previamente. | Al convertir 72 °C en temperatura_alta se pierde el valor exacto. |
| Autómata | Permite reconocer patrones secuenciales y persistencia de anomalías. | Solo reconoce patrones definidos mediante sus estados y transiciones. | La secuencia N/A no conserva los valores exactos de las métricas. |

## Conversión entre representaciones

Los valores numéricos del monitoreo pueden convertirse en hechos simbólicos utilizando umbrales. Por ejemplo, una temperatura igual o superior a 70 °C se transforma en el hecho `temperatura_alta`.

De forma similar, varias observaciones del servidor pueden convertirse en una secuencia de estados N y A. El autómata utiliza dicha secuencia para identificar persistencia en el comportamiento anómalo.

## Limitaciones

- Los valores de referencia y los umbrales son definidos para la práctica y deberían ajustarse con datos reales.
- Una representación simbólica simplifica los valores originales.
- El autómata solamente considera estados N y A, por lo que no diferencia tipos de anomalías.
- La distancia numérica indica diferencia, pero por sí sola no determina la causa de la anomalía.

## Conclusión

La misma situación de un servidor puede representarse de diferentes maneras. La representación numérica permite realizar comparaciones matemáticas; la simbólica facilita la explicación mediante hechos y reglas; y el autómata permite reconocer patrones temporales.

La combinación de estas representaciones complementa el sistema de detección de anomalías desarrollado durante el semestre.
