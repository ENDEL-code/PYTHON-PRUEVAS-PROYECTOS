#!/usr/bin/env python3
import os, json, datetime, threading,requests
from flask import Flask, request, jsonify, send_file
from colorama import init, Fore, Style
from plyer import notification

init(autoreset=True)
ARCHIVO = "tareas.json"
ANDROID_IP = "192.168.0.67" 
""  # ← Cambia esto por la IP de tu teléfono
app = Flask(__name__)

materias = {
    "ESP": "ivon meza molina",
    "MAT": "ismenia bolaños soto",
    "HISTORIA": "yolanda vazquez",
    "INGLES": "angeles martines",
    "ARTE": "carmina saymes rueda",
    "TUTOR": "jose luis morales cruz",
    "QUIMICA": "jose luis morales cruz",
    "TALLER": "norma pradel blancas",
    "EDU.FISICA": "viridiana isabel rico alvarez",
    "FCYE": "norma"
}

horario = {
    "07:15 - 08:20": ["MAT", "QUIMICA", "FCYE", "QUIMICA", "HISTORIA"],
    "08:20 - 09:10": ["TUTOR", "TALLER", "ESP", "HISTORIA", "ESP"],
    "09:10 - 10:00": ["HISTORIA", "MAT", "QUIMICA", "CURRICULAR", "MAT"],
    "10:00 - 10:50": ["QUIMICA", "TALLER", "MAT", "EDU.FISICA", "ARTE"],
    "11:10 - 12:00": ["ESP", "ESP", "TALLER", "INGLES", "FCYE"],
    "12:00 - 12:50": ["INGLES", "HISTORIA", "ARTE", "ESP", "QUIMICA"],
    "12:50 - 13:40": ["ARTE", "INGLES", "EDU.FISICA", "MAT", "QUIMICA"]
}
dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]

def cargar_tareas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_tareas(tareas):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=2, ensure_ascii=False)

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

def show_notification(tasks):
    nombres = ", ".join(t["nombre"] for t in tasks)
    notification.notify(title="📌 Tareas para mañana", message=nombres or "Tienes tareas para mañana", timeout=10)

def schedule_notifications(tareas):
    hoy = datetime.date.today()
    manana = hoy + datetime.timedelta(days=1)
    due = [t for t in tareas if not t.get("completada", False) and datetime.date.fromisoformat(t["fecha"]) == manana]
    if not due:
        return
    alerta = datetime.datetime.combine(manana, datetime.time(hour=15))
    segundos = (alerta - datetime.datetime.now()).total_seconds()
    if segundos <= 0:
        show_notification(due)
    else:
        threading.Timer(segundos, show_notification, args=(due,)).start()

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + r"""
    _____     ____   ____  ____   ___
    |  _ \   |  _ \ |  _ \ |_ _|  / _ \
    | | | |  | |_) || |_) | | |  | | | |
    | |_| |  |  __/ |  __/  | |  | |_| |
    |____/   |_|    |_|    |___|  \___/
                                
           ENDEL-DESKTOP           
    """)

def mostrar_tareas(tareas):
    banner()
    print(Fore.WHITE + Style.BRIGHT + "📋 TAREAS:\n")
    if not tareas:
        print(Fore.LIGHTBLACK_EX + "— No hay tareas —")
        return
    for i, t in enumerate(tareas, 1):
        estado = Fore.GREEN + "✔" if t.get("completada") else Fore.RED + "✘"
        prioridad = {"alta": Fore.RED + "🔴", "media": Fore.YELLOW + "🟡", "baja": Fore.GREEN + "🟢"}.get(t.get("prioridad"), Fore.WHITE + "⚪")
        fecha_txt = t.get("fecha") if "fecha" in t else t.get("fecha_txt", "—")
        print(f"{Fore.CYAN}{i:>2}. {estado} {Fore.WHITE}{t['nombre']} {Fore.LIGHTBLACK_EX}({fecha_txt}) {prioridad}")

def mostrar_horario():
    banner()
    print(Fore.WHITE + Style.BRIGHT + "📆 HORARIO ESCOLAR:\n")
    print(Fore.LIGHTBLACK_EX + "Hora".ljust(18) + "".join(f"{d:<12}" for d in dias))
    print(Fore.LIGHTBLACK_EX + "-" * 80)
    for hora, materias_dia in horario.items():
        fila = Fore.CYAN + hora.ljust(18)
        fila += "".join(f"{m:<12}" for m in materias_dia)
        print(fila)
    input(Fore.WHITE + "\nEnter para continuar…")

def agregar_tarea(tareas):
    banner()
    print(Fore.WHITE + Style.BRIGHT + "➕ NUEVA TAREA\n")

    print("📚 Materias disponibles:")
    for i, (clave, maestro) in enumerate(materias.items(), 1):
        print(f"{Fore.CYAN}{i:>2}. {clave} ({maestro})")

    try:
        seleccion = int(input(Fore.WHITE + "\n👉 Elige el número de la materia: ").strip()) - 1
        materia_clave = list(materias.keys())[seleccion]
    except Exception:
        print(Fore.RED + "\n❌ Selección inválida. Se usará 'ESP'.")
        materia_clave = "ESP"

    nombre = input("📝 Nombre de la tarea: ").strip() or "— Sin título —"

    fecha_input = input("📅 Fecha (dd/mm/aaaa): ").strip()
    try:
        fecha_obj = datetime.datetime.strptime(fecha_input, "%d/%m/%Y")
        fecha_iso = fecha_obj.date().isoformat()
    except Exception:
        print(Fore.RED + "\n❌ Fecha inválida. Se usará la de hoy.")
        fecha_iso = datetime.date.today().isoformat()

    prioridad = input("⚡ Prioridad (alta/media/baja): ").strip().lower()
    prioridad = prioridad if prioridad in ("alta", "media", "baja") else "media"

    tareas.append({
        "nombre": f"{materia_clave} - {nombre}",
        "fecha": fecha_iso,
        "prioridad": prioridad,
        "completada": False
    })

    guardar_tareas(tareas)
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

def descargar_desde_android():
    try:
        r = requests.get(f"http://{ANDROID_IP}:5000/get_tareas", timeout=6)
        with open(ARCHIVO, "wb") as f:
            f.write(r.content)
        print(Fore.GREEN + "📥 Tareas descargadas desde Android.")
    except Exception:
        print(Fore.RED + "⚠️ No se pudo conectar al teléfono.")
    input("Enter para continuar…")

def enviar_a_android():
    try:
        tareas = cargar_tareas()
        r = requests.post(f"http://{ANDROID_IP}:5000/update_tareas", json=tareas, timeout=6)
        print(Fore.GREEN + "📤 Tareas enviadas a Android.")
    except Exception:
        print(Fore.RED + "⚠️ No se pudo enviar al teléfono.")
    input("Enter para continuar…")

def menu():
    tareas = cargar_tareas()
    schedule_notifications(tareas)
    while True:
        banner()
        print(Fore.WHITE + Style.BRIGHT + "📂 MENÚ PRINCIPAL\n")
        print(Fore.CYAN + " 1️⃣  Ver tareas")
        print(Fore.YELLOW + " 2️⃣  Agregar tarea")
        print(Fore.GREEN + " 3️⃣  Marcar como completada")
        print(Fore.RED + " 4️⃣  Borrar tarea")
        print(Fore.MAGENTA + " 5️⃣  Descargar desde Android")
        print(Fore.MAGENTA + " 6️⃣  Enviar a Android")
        print(Fore.BLUE + " 7️⃣  Ver horario escolar")
        print(Fore.LIGHTBLACK_EX + " 8️⃣  Salir\n")
        opc = input(Fore.WHITE + "👉 Elige una opción: ").strip()
        tareas = cargar_tareas()
        if opc == "1":
            mostrar_tareas(tareas); input("Enter…")
        elif opc == "2":
            agregar_tarea(tareas)
        elif opc == "3":
            completar_tarea(tareas)
        elif opc == "4":
            borrar_tarea(tareas)
        elif opc == "5":
            descargar_desde_android()
        elif opc == "6":
            enviar_a_android()
        elif opc == "7":
            mostrar_horario()
        elif opc == "8":
            print(Fore.LIGHTBLACK_EX + "\n👋 Cerrando gestor desktop."); break
        else:
            print(Fore.RED + "\n❌ Opción inválida."); input("Enter…")

if __name__ == "__main__":
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True).start()
    menu()
#power by endel 
# no tocar funciona y no c pq
# Fin del archivo
