#!/usr/bin/env python3
import os
import json
import datetime
import threading
from colorama import init, Fore, Style
from plyer import notification

init(autoreset=True)
ARCHIVO = "tareas.json"

def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

def cargar_tareas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return []

def guardar_tareas(tareas):
    with open(ARCHIVO, "w") as f:
        json.dump(tareas, f, indent=2)

def banner():
    clear_screen()
    logo = r"""
    _____     ____   ____  ____   ___
    |  _ \   |  _ \ |  _ \ |_ _|  / _ \
    | | | |  | |_) || |_) | | |  | | | |
    | |_| |  |  __/ |  __/  | |  | |_| |
    |____/   |_|    |_|    |___|  \___/
                                
           ENDEL-PROGRAMER           
    """
    print(Fore.CYAN + logo)

def show_notification(tasks):
    nombres = ", ".join(t["nombre"] for t in tasks)
    notification.notify(
        title="📌 Tareas para mañana",
        message=nombres,
        timeout=10
    )

def schedule_notifications(tareas):
    hoy = datetime.date.today()
    manana = hoy + datetime.timedelta(days=1)
    due = [
        t for t in tareas
        if not t["completada"]
        and datetime.date.fromisoformat(t["fecha"]) == manana
    ]
    if not due:
        return
    ahora = datetime.datetime.now()
    alerta = datetime.datetime.combine(manana, datetime.time(hour=15))
    segundos = (alerta - ahora).total_seconds()
    if segundos <= 0:
        show_notification(due)
    else:
        threading.Timer(segundos, show_notification, args=(due,)).start()

def mostrar_tareas(tareas):
    banner()
    print(Fore.WHITE + "📋 TAREAS PENDIENTES:\n")
    if not tareas:
        print("   — No hay tareas —")
    for i, t in enumerate(tareas, 1):
        estado = Fore.GREEN+"✔" if t["completada"] else Fore.RED+"✘"
        color = {
            "alta": Fore.RED,
            "media": Fore.YELLOW,
            "baja": Fore.GREEN
        }.get(t["prioridad"], Fore.WHITE)
        print(f" {i}. {estado} {t['nombre']} ({t['fecha']}) {color}[{t['prioridad'].upper()}]")

def agregar_tarea(tareas):
    banner()
    nombre = input("Nombre: ").strip() or "— Sin título —"
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    prioridad = input("Prioridad (alta/media/baja): ").strip().lower()
    tareas.append({
        "nombre": nombre,
        "fecha": fecha or datetime.date.today().isoformat(),
        "prioridad": prioridad if prioridad in ("alta","media","baja") else "media",
        "completada": False
    })
    guardar_tareas(tareas)
    print(Fore.GREEN + "\n✅ Tarea agregada.")
    input("Enter para continuar…")

def completar_tarea(tareas):
    mostrar_tareas(tareas)
    try:
        i = int(input("\nNúmero a completar: ")) - 1
        tareas[i]["completada"] = True
        guardar_tareas(tareas)
        print(Fore.GREEN + "\n🎉 Completada.")
    except:
        print(Fore.RED + "\n¡Entrada inválida!")
    input("Enter para continuar…")

def menu():
    tareas = cargar_tareas()
    schedule_notifications(tareas)

    while True:
        banner()
        print("1. Ver tareas")
        print("2. Agregar tarea")
        print("3. Completar tarea")
        print("4. Salir\n")
        opc = input("Elige opción: ").strip()
        if opc=="1":
            mostrar_tareas(tareas); input("Enter…")
        elif opc=="2":
            agregar_tarea(tareas)
        elif opc=="3":
            completar_tarea(tareas)
        elif opc=="4":
            break
        else:
            print(Fore.RED + "Opción inválida."); input("Enter…")

if __name__ == "__main__":
    menu()
