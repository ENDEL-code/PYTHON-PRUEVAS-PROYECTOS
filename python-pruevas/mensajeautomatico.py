import pyautogui  # type: ignore
import time

cantidad = 10
mensajes_error = [
    "ENDEL-BOT: Mensaje script-ERROR numero {} error critico",
    "ENDEL-BOT: Informando problema a soporte tecnico (Endel-Soport)"
]
mensajes_finales = [
    "ENDEL-BOT: Demasiados errores continuos",
    "ENDEL-BOT: Cerrando operaciones...",
    "ENDEL-BOT: Nos vemos",
    "ENDEL-BOT: Endel-Soport contactado por favor espere"
]

def escribir_lento(texto, pausa=0.06):
    time.sleep(0.3)  # pequeña pausa antes de escribir
    pyautogui.write(texto, interval=pausa)
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(0.5)

print("Enfoca la ventana de destino. Comenzamos en 5 segundos...")
time.sleep(5)

# Bucle principal
for i in range(cantidad):
    escribir_lento(mensajes_error[0].format(i + 1))
    escribir_lento(mensajes_error[1])
    print(f"Mensaje {i + 1} enviado correctamente")

# Mensajes finales
for mensaje in mensajes_finales:
    escribir_lento(mensaje)

print("✅ Todo está desactivado. Es seguro modificar ahora.")
print("_________________________________________")
