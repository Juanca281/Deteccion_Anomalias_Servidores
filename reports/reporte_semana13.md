# Reporte Semana 13 - Ingeniería del conocimiento

## Proyecto

**ServidorIA - Detección de anomalías en servidores**

## 1. Problema del dominio

El proyecto trabaja con telemetrías y evidencias que pueden indicar degradación o riesgo operativo en un servidor. La funcionalidad seleccionada para Semana 13 consiste en **razonar sobre hechos técnicos ya identificados** y determinar si existe evidencia suficiente para recomendar mantenimiento y escalamiento.

El motor no reemplaza la medición de CPU, RAM, disco, latencia o errores. Su responsabilidad es tomar hechos simbólicos y aplicar reglas explícitas, manteniendo una traza de cada conclusión.

## 2. Conceptos y hechos

Los hechos iniciales posibles son:

- `cpu_alta`
- `ram_alta`
- `latencia_alta`
- `errores_altos`
- `disco_critico`

Las conclusiones que puede producir el motor son:

- `sobrecarga_recursos`
- `degradacion_servicio`
- `riesgo_critico`
- `incidente_prioridad_alta`
- `escalar_soporte`
- `mantenimiento_recomendado`

## 3. Reglas lógicas

| Regla | Premisas | Conclusión |
|---|---|---|
| R1 | `cpu_alta ∧ ram_alta` | `sobrecarga_recursos` |
| R2 | `latencia_alta ∧ errores_altos` | `degradacion_servicio` |
| R3 | `disco_critico ∧ sobrecarga_recursos` | `riesgo_critico` |
| R4 | `sobrecarga_recursos ∧ degradacion_servicio` | `incidente_prioridad_alta` |
| R5 | `riesgo_critico ∧ incidente_prioridad_alta` | `escalar_soporte` |
| R6 | `escalar_soporte` | `mantenimiento_recomendado` |

Estas reglas son una simplificación académica del dominio y no constituyen una política operativa universal para todos los servidores.

## 4. Motor de inferencia

La función `inferir()` utiliza **encadenamiento hacia adelante**:

1. Copia los hechos iniciales para no modificarlos.
2. Recorre la base de reglas.
3. Si todas las premisas están presentes y la conclusión es nueva, agrega la conclusión.
4. Registra la regla aplicada, sus premisas y la conclusión.
5. Repite el proceso mientras aparezcan hechos nuevos.
6. Termina cuando una vuelta completa no produce cambios.

La verificación `conclusion not in hechos` evita conclusiones duplicadas y contribuye a que el proceso termine incluso cuando existen reglas cíclicas.

## 5. Escenarios funcionales

### Caso A - conclusión demostrada

Hechos iniciales:

`cpu_alta`, `ram_alta`, `latencia_alta`, `errores_altos`, `disco_critico`.

Traza esperada:

1. R1 deriva `sobrecarga_recursos`.
2. R2 deriva `degradacion_servicio`.
3. R3 deriva `riesgo_critico`.
4. R4 deriva `incidente_prioridad_alta`.
5. R5 deriva `escalar_soporte`.
6. R6 deriva `mantenimiento_recomendado`.

Resultado: **mantenimiento recomendado DEMOSTRADO**.

### Caso B - conclusión no demostrada

Se utilizan los mismos hechos excepto `disco_critico`.

R1, R2 y R4 todavía pueden ejecutarse, pero R3 no puede derivar `riesgo_critico`. Como consecuencia, R5 y R6 tampoco pueden activarse.

Resultado: **mantenimiento recomendado NO DEMOSTRADO con los hechos disponibles**.

Esto no significa que el servidor esté definitivamente sano. Solo significa que la conclusión no puede obtenerse con la evidencia presente y las reglas declaradas.

## 6. Pruebas con unittest

`test_motor_inferencia.py` comprueba:

- Caso A demostrado.
- Caso B no demostrado.
- Conservación de los hechos iniciales.
- Ausencia de conclusiones duplicadas.
- Terminación ante un ciclo artificial de reglas.

Ejecutar:

```powershell
python semana13\test_motor_inferencia.py
```

## 7. Trazabilidad

Cada elemento de la traza conserva:

- Iteración.
- Identificador de regla.
- Premisas utilizadas.
- Conclusión obtenida.
- Descripción de la regla.

Esto permite explicar durante la sustentación exactamente **por qué** apareció cada nuevo hecho.

## 8. Limitaciones

- Solo usa reglas positivas.
- No implementa negación lógica.
- No maneja probabilidades ni incertidumbre.
- No decide umbrales de telemetría por sí mismo.
- No aprende reglas automáticamente.
- Las reglas deben ser revisadas y validadas antes de una aplicación operativa real.

## 9. Conclusión

Semana 13 incorpora al proyecto un componente explicable de ingeniería del conocimiento. A diferencia de un modelo entrenado, el motor trabaja con reglas explícitas y permite reconstruir toda la cadena de inferencias. Esto complementa las etapas anteriores del proyecto, en las que se detectaron y clasificaron patrones de anomalías.
