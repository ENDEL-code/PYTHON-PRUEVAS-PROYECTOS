import os
import json
import requests
import threading
from datetime import datetime, date, timedelta, time as dtime
from flask import Flask, request, jsonify, send_file
from colorama import init, Fore, Style

# notificaciones
try:
    from plyer import notification
except Exception:
    notification = None

init(autoreset=True)
ARCHIVO = "tareas.json"
PC_IP = "192.168.0.9"  # ← Cambia esto por la IP de tu PC

app = Flask(__name__)

MATERIAS = {
    "ESP": "ivon meza molina",
    "MAT": "ismenia bolaños soto",
    "HISTORIA": "yolanda vazquez",
    "INGLES": "angeles martines",
    "ARTE": "carmina saymes rueda",
    "TUTOR": "jose luis morales cruz",
    "QUIMICA": "jose luis morales cruz",
    "TALLER": "norma pradel blancas",
    "EDU.FISICA": "viridiana isabel rico alvarez",
    "FCYE": "--"
}

HORARIO = {
    "07:15 - 08:20": ["MAT", "QUIMICA", "FCYE", "QUIMICA", "HISTORIA"],
    "08:20 - 09:10": ["TUTOR", "TALLER", "ESP", "HISTORIA", "ESP"],
    "09:10 - 10:00": ["HISTORIA", "MAT", "QUIMICA", "CURRICULAR", "MAT"],
    "10:00 - 10:50": ["QUIMICA", "TALLER", "MAT", "EDU.FISICA", "ARTE"],
    "11:10 - 12:00": ["ESP", "ESP", "TALLER", "INGLES", "FCYE"],
    "12:00 - 12:50": ["INGLES", "HISTORIA", "ARTE", "ESP", "QUIMICA"],
    "12:50 - 13:40": ["ARTE", "INGLES", "EDU.FISICA", "MAT", "QUIMICA"]
}
DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]

def banner():
    os.system("clear")
    logo = r"""
    _____     ____   ____  ____   ___
    |  _ \   |  _ \ |  _ \ |_ _|  / _ \
    | | | |  | |_) || |_) | | |  | | | |
    | |_| |  |  __/ |  __/  | |  | |_| |
    |____/   |_|    |_|    |___|  \___/
                                
           ENDEL-MOBILE            
    """
    print(Fore.CYAN + logo)

def cargar_tareas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_tareas(tareas):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=2, ensure_ascii=False)

def sincronizar_desde_pc():
    try:
        r = requests.get(f"http://{PC_IP}:5000/get_tareas", timeout=6)
        with open(ARCHIVO, "wb") as f:
            f.write(r.content)
        print(Fore.GREEN + "📥 Tareas descargadas desde PC.")
    except Exception:
        print(Fore.RED + "⚠️ No se pudo conectar al servidor.")

def enviar_a_pc():
    try:
        tareas = cargar_tareas()
        r = requests.post(f"http://{PC_IP}:5000/update_tareas", json=tareas, timeout=6)
        print(Fore.GREEN + "📤 Tareas enviadas a PC.")
    except Exception:
        print(Fore.RED + "⚠️ No se pudo enviar al servidor.")

@app.route("/get_tareas", methods=["GET"])
def get_tareas():
    if os.path.exists(ARCHIVO):
        return send_file(ARCHIVO)
    return jsonify([])

@app.route("/update_tareas", methods=["POST"])
def update_tareas():
    tareas = request.get_json()
    guardar_tareas(tareas)
    return jsonify({"status": "ok"})

def parse_fecha_ddmmaa(texto):
    texto = texto.strip()
    try:
        partes = texto.split("/")
        if len(partes) != 3:
            return None
        d, m, a = partes
        d = int(d); m = int(m); a = int(a)
        if a < 100:
            a += 2000
        return date(a, m, d)
    except Exception:
        return None

def fecha_a_ddmmaa(fecha):
    return fecha.strftime("%d/%m/%y")

def show_notification(tasks):
    if notification is None:
        return
    nombres = ", ".join(t["nombre"] for t in tasks)
    notification.notify(title="📌 Tareas para mañana", message=nombres or "Tienes tareas para mañana", timeout=10)

def schedule_notifications(tareas):
    hoy = date.today()
    manana = hoy + timedelta(days=1)
    due = [t for t in tareas if (not t.get("completada", False)) and parse_fecha_ddmmaa(t.get("fecha_txt", "")) == manana]
    if not due:
        return
    ahora = datetime.now()
    alerta_dt = datetime.combine(manana, dtime(hour=15, minute=0))
    segundos = (alerta_dt - ahora).total_seconds()
    if segundos <= 0:
        show_notification(due)
    else:
        threading.Timer(segundos, show_notification, args=(due,)).start()

def mostrar_tareas(tareas):
    banner()
    print(Fore.WHITE + Style.BRIGHT + "📋 TAREAS:\n")
    if not tareas:
        print(Fore.LIGHTBLACK_EX + "— No hay tareas —")
        return
    for i, t in enumerate(tareas, 1):
        estado = Fore.GREEN + "✔" if t.get("completada") else Fore.RED + "✘"
        prioridad_color = {"alta": Fore.RED + "🔴", "media": Fore.YELLOW + "🟡", "baja": Fore.GREEN + "🟢"}.get(t.get("prioridad"), Fore.WHITE + "⚪")
        fecha_txt = t.get("fecha_txt") or t.get("fecha") or "—"
        materia = t.get("materia", "—")
        maestro = t.get("maestro", "—")
        print(f"{Fore.CYAN}{i:>2}. {estado} {Fore.WHITE}{t['nombre']} {Fore.LIGHTBLACK_EX}({fecha_txt}) {prioridad_color} {Fore.MAGENTA}{materia} {Fore.LIGHTBLACK_EX}({maestro})")

def mostrar_horario():
    banner()
    print(Fore.WHITE + Style.BRIGHT + "📆 HORARIO ESCOLAR:\n")
    print(Fore.LIGHTBLACK_EX + "Hora".ljust(18) + "".join(f"{d:<12}" for d in DIAS))
    print(Fore.LIGHTBLACK_EX + "-" * 80)
    for hora, materias_dia in HORARIO.items():
        fila = Fore.CYAN + hora.ljust(18)
        fila += "".join(f"{m:<12}" for m in materias_dia)
        print(fila)
    input(Fore.WHITE + "\nEnter para continuar…")

def elegir_materia():
    banner()
    print(Fore.WHITE + Style.BRIGHT + "📚 Elige la materia:\n")
    claves = list(MATERIAS.keys())
    for i, k in enumerate(claves, 1):
        print(f" {i}. {k} - {MATERIAS[k]}")
    print("\n 0. Cancelar")
    try:
        sel = int(input("\nElige número: ").strip())
    except Exception:
        return None, None
    if sel == 0:
        return None, None
    if 1 <= sel <= len(claves):
        clave = claves[sel-1]
        return clave, MATERIAS[clave]
    return None, None

def agregar_tarea(tareas):
    banner()
    print(Fore.WHITE + Style.BRIGHT + "➕ NUEVA TAREA\n")
    nombre = input("📝 Nombre: ").strip() or "— Sin título —"
    while True:
        fecha_input = input("📅 Fecha (dd/mm/aa): ").strip()
        fecha = parse_fecha_ddmmaa(fecha_input)
        if fecha:
            break
        print(Fore.RED + "Formato inválido. Ejemplo: 05/10/25")
    materia, maestro = elegir_materia()
    if materia is None:
        print(Fore.YELLOW + "\nOperación cancelada.")
        input("Enter para continuar…")
        return
    prioridad = input("⚡ Prioridad (alta/media/baja) [media]: ").strip().lower()
    prioridad = prioridad if prioridad in ("alta", "media", "baja") else "media"
    tarea = {
        "nombre": nombre,
        "fecha": fecha.isoformat(),
        "fecha_txt": fecha_a_ddmmaa(fecha),
        "prioridad": prioridad,
        "completada": False,
        "materia": materia,
        "maestro": maestro
    }
    tareas.append(tarea)
    guardar_tareas(tareas)
    schedule_notifications(tareas)
    print(Fore.GREEN + "\n✅ Tarea agregada.")
    input("Enter para continuar…")

def completar_tarea(tareas):
    mostrar_tareas(tareas)
    try:
        i = int(input("\n✔ Número de tarea a completar: ")) - 1
        tareas[i]["completada"] = True
        guardar_tareas(tareas)
        print(Fore.GREEN + "\n🎉 Tarea marcada como completada.")
    except Exception:
        print(Fore.RED + "\n❌ Entrada inválida.")
    input("Enter para continuar…")

def borrar_tarea(tareas):
    mostrar_tareas(tareas)
    try:
        i = int(input("\n🗑️ Número de tarea a borrar: ")) - 1
        tarea = tareas.pop(i)
        guardar_tareas(tareas)
        print(Fore.YELLOW + f"\n🧹 Tarea '{tarea['nombre']}' eliminada.")
    except Exception:
        print(Fore.RED + "\n❌ Entrada inválida.")
    input("Enter para continuar…")

def menu():
    tareas = cargar_tareas()
    changed = False
    for t in tareas:
        if "fecha_txt" not in t and "fecha" in t:
            try:
                d = datetime.fromisoformat(t["fecha"]).date()
                t["fecha_txt"] = fecha_a_ddmmaa(d)
                changed = True
            except Exception:
                pass
    if changed:
        guardar_tareas(tareas)

    schedule_notifications(tareas)

    while True:
        banner()
        print(Fore.WHITE + Style.BRIGHT + "📱 GESTOR DE TAREAS MÓVIL\n")
        print(Fore.YELLOW + " 1️⃣  Ver tareas")
        print(Fore.GREEN + " 2️⃣  Agregar tarea")
        print(Fore.BLUE + " 3️⃣  Marcar como completada")
        print(Fore.RED + " 4️⃣  Borrar tarea")
        print(Fore.MAGENTA + " 5️⃣  Descargar desde PC")
        print(Fore.MAGENTA + " 6️⃣  Enviar a PC")
        print(Fore.BLUE + " 7️⃣  Ver horario escolar")
        print(Fore.LIGHTBLACK_EX + " 8️⃣  Salir\n")

        opc = input(Fore.WHITE + "👉 Elige una opción: ").strip()
        tareas = cargar_tareas()

        if opc == "1":
            mostrar_tareas(tareas)
            input(Fore.MAGENTA + "\n🔁 Enter para volver al menú…")
        elif opc == "2":
            agregar_tarea(tareas)
        elif opc == "3":
            completar_tarea(tareas)
        elif opc == "4":
            borrar_tarea(tareas)
        elif opc == "5":
            sincronizar_desde_pc()
            input("Enter para continuar…")
        elif opc == "6":
            enviar_a_pc()
            input("Enter para continuar…")
        elif opc == "7":
            mostrar_horario()
        elif opc == "8":
            print(Fore.LIGHTBLACK_EX + "\n👋 Cerrando gestor móvil.")
            break
        else:
            print(Fore.RED + "\n❌ Opción inválida.")
            input("Enter para continuar…")

if __name__ == "__main__":
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True).start()
    menu()
