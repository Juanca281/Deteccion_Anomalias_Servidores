"""
Semana 02 - Fundamentos de Python aplicados al proyecto.

Proyecto:
Detección de anomalías operativas en servidores

Descripción:
Este módulo aplica los fundamentos de Python vistos durante la
Semana 02 a un contexto de monitoreo de servidores.

Se trabajan:
- Variables y tipos de datos
- Entrada de datos
- Operadores
- Condicionales
- Funciones
- Estructuras de datos
- Clasificación básica de métricas
"""


# ============================================================
# 1. DATOS DEL SERVIDOR
# ============================================================

nombre_servidor = "Servidor-Web-01"

cpu = 45.5
memoria_ram = 62.0
uso_disco = 48.5
latencia = 85.0
solicitudes_minuto = 150
errores = 3

servidor_activo = True


# ============================================================
# 2. MOSTRAR INFORMACIÓN DEL SERVIDOR
# ============================================================

print("=" * 50)
print("MONITOREO DE SERVIDOR")
print("=" * 50)

print(f"Servidor: {nombre_servidor}")
print(f"CPU: {cpu}%")
print(f"Memoria RAM: {memoria_ram}%")
print(f"Uso de disco: {uso_disco}%")
print(f"Latencia: {latencia} ms")
print(f"Solicitudes por minuto: {solicitudes_minuto}")
print(f"Errores: {errores}")
print(f"Servidor activo: {servidor_activo}")


# ============================================================
# 3. OPERACIONES BÁSICAS
# ============================================================

recursos_promedio = (
    cpu + memoria_ram + uso_disco
) / 3

total_eventos = solicitudes_minuto + errores

print("\n" + "=" * 50)
print("ANÁLISIS BÁSICO")
print("=" * 50)

print(f"Promedio de utilización de recursos: {recursos_promedio:.2f}%")
print(f"Total de eventos registrados: {total_eventos}")


# ============================================================
# 4. CONDICIONALES
# ============================================================

print("\n" + "=" * 50)
print("ESTADO DE LOS RECURSOS")
print("=" * 50)

if cpu >= 90:
    print("⚠️ CPU: nivel crítico")
elif cpu >= 75:
    print("⚠️ CPU: nivel alto")
else:
    print("✅ CPU: nivel normal")


if memoria_ram >= 90:
    print("⚠️ RAM: nivel crítico")
elif memoria_ram >= 75:
    print("⚠️ RAM: nivel alto")
else:
    print("✅ RAM: nivel normal")


if uso_disco >= 90:
    print("⚠️ Disco: nivel crítico")
elif uso_disco >= 75:
    print("⚠️ Disco: nivel alto")
else:
    print("✅ Disco: nivel normal")


if latencia >= 500:
    print("⚠️ Latencia: nivel crítico")
elif latencia >= 200:
    print("⚠️ Latencia: nivel alto")
else:
    print("✅ Latencia: nivel normal")


# ============================================================
# 5. FUNCIÓN PARA EVALUAR UN SERVIDOR
# ============================================================

def evaluar_servidor(cpu, memoria_ram, uso_disco, latencia):
    """
    Evalúa las principales métricas de un servidor.

    Retorna:
        str: estado general del servidor.
    """

    metricas_criticas = 0

    if cpu >= 90:
        metricas_criticas += 1

    if memoria_ram >= 90:
        metricas_criticas += 1

    if uso_disco >= 90:
        metricas_criticas += 1

    if latencia >= 500:
        metricas_criticas += 1

    if metricas_criticas >= 2:
        return "ANOMALÍA CRÍTICA"

    elif metricas_criticas == 1:
        return "ADVERTENCIA"

    else:
        return "NORMAL"


estado_servidor = evaluar_servidor(
    cpu,
    memoria_ram,
    uso_disco,
    latencia
)

print("\n" + "=" * 50)
print("RESULTADO DE LA EVALUACIÓN")
print("=" * 50)

print(f"Estado del servidor: {estado_servidor}")


# ============================================================
# 6. ESTRUCTURA DE DATOS
# ============================================================

metricas = {
    "cpu": cpu,
    "memoria_ram": memoria_ram,
    "uso_disco": uso_disco,
    "latencia": latencia,
    "solicitudes_minuto": solicitudes_minuto,
    "errores": errores
}

print("\n" + "=" * 50)
print("MÉTRICAS REGISTRADAS")
print("=" * 50)

for nombre, valor in metricas.items():
    print(f"{nombre}: {valor}")


# ============================================================
# 7. RESUMEN
# ============================================================

print("\n" + "=" * 50)
print("RESUMEN")
print("=" * 50)

if estado_servidor == "NORMAL":
    print("✅ El servidor presenta un comportamiento normal.")

elif estado_servidor == "ADVERTENCIA":
    print("⚠️ El servidor presenta una métrica que requiere atención.")

else:
    print("🚨 Se detectaron múltiples métricas en niveles críticos.")
    print("Se recomienda revisar el estado del servidor.")