
import psutil
import platform
import socket
from datetime import datetime

def obtener_datos_reales():
    datos = {
        "Nombre del host": socket.gethostname(),
        "Sistema operativo": platform.system() + " " + platform.release(),
        "Arquitectura": platform.machine(),
        "Núcleos activos": psutil.cpu_count(logical=True),
        "Frecuencia base CPU": f"{psutil.cpu_freq().max:.2f} MHz",
        "Memoria RAM total": f"{round(psutil.virtual_memory().total / (1024**2))} MB",
        "Memoria RAM disponible": f"{round(psutil.virtual_memory().available / (1024**2))} MB",
        "Almacenamiento total": f"{round(psutil.disk_usage('/').total / (1024**3), 1)} GB",
        "Espacio libre": f"{round(psutil.disk_usage('/').free / (1024**3), 1)} GB",
        "Uso de CPU (%)": psutil.cpu_percent(interval=1),
        "Temperatura CPU": "N/A (requiere sensores específicos)",
        "Dirección IP local": socket.gethostbyname(socket.gethostname()),
        "Fecha/hora local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Tiempo activo del sistema": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
    }
    return datos

def imprimir_datos(datos):
    print("[CAPTURA DE DATOS DEL SISTEMA]\n")
    for clave, valor in datos.items():
        print(f"> {clave}: {valor}")
    print("\n[FIN DE CAPTURA]")

# Ejecutar
datos = obtener_datos_reales()
imprimir_datos(datos)
