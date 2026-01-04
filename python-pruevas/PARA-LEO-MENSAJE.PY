import pyautogui # type: ignore
import time

cantidad = 10

time.sleep(5)
for i in range(cantidad):
    mensaje = f"ENDEL-bot: mensaje {i+1} enviado  "
    pyautogui.typewrite(mensaje)
    pyautogui.press("enter")
