import tkinter as tk
from tkinter import messagebox
import pyautogui
import pygetwindow as gw
import time
import json
import os

CONFIG_FILE = "endel_bot_config.json"
PREFIX = "ENDEL-bot: "

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"search_pos": None, "message_pos": None}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def countdown_and_capture(label_text):
    info = tk.Toplevel(root)
    info.title("Calibración")
    lbl = tk.Label(info, text=f"{label_text}\nColoca el cursor sobre el objetivo.\nCaptura en 3…")
    lbl.pack(padx=12, pady=12)
    root.update()
    for i in [2,1]:
        time.sleep(1)
        lbl.config(text=f"{label_text}\nColoca el cursor sobre el objetivo.\nCaptura en {i}…")
        root.update()
    time.sleep(1)
    info.destroy()
    pos = pyautogui.position()
    return (pos.x, pos.y)

def calibrate_search():
    pos = countdown_and_capture("Apunta a la barra de búsqueda de chats en WhatsApp")
    cfg = load_config()
    cfg["search_pos"] = pos
    save_config(cfg)
    messagebox.showinfo("Calibración", f"Posición de búsqueda guardada: {pos}")

def calibrate_message():
    pos = countdown_and_capture("Apunta al cuadro de texto 'Escribe un mensaje'")
    cfg = load_config()
    cfg["message_pos"] = pos
    save_config(cfg)
    messagebox.showinfo("Calibración", f"Posición de mensaje guardada: {pos}")

def focus_whatsapp():
    windows = gw.getWindowsWithTitle("WhatsApp")
    if not windows:
        return False
    win = windows[0]
    if win.isMinimized:
        win.restore()
        time.sleep(0.3)
    win.activate()
    time.sleep(0.3)
    return True

def send_to_whatsapp(contact_name, message_text):
    cfg = load_config()
    sp = cfg.get("search_pos")
    mp = cfg.get("message_pos")
    if not mp:
        messagebox.showwarning("Falta calibrar", "Calibra el cuadro de mensaje antes de enviar.")
        return

    if not focus_whatsapp():
        messagebox.showerror("WhatsApp no encontrado", "No se detectó la ventana 'WhatsApp'. Ábrela y vuelve a intentar.")
        return

    # Si se especifica contacto, buscarlo
    if contact_name:
        if not sp:
            messagebox.showwarning("Falta calibrar", "Calibra la barra de búsqueda si quieres cambiar de contacto.")
            return
        pyautogui.click(sp[0], sp[1])
        pyautogui.hotkey("ctrl", "a")
        pyautogui.typewrite(contact_name, interval=0.02)
        time.sleep(0.4)
        pyautogui.press("enter")

    # Escribir mensaje en el chat activo
    pyautogui.click(mp[0], mp[1])
    final_text = f"{PREFIX}{message_text}"
    pyautogui.typewrite(final_text, interval=0.02)
    pyautogui.press("enter")

def on_send(event=None):
    contact = contact_var.get().strip()
    msg = message_var.get().strip()
    if not msg:
        messagebox.showwarning("Mensaje vacío", "Escribe el mensaje para enviar.")
        return
    send_to_whatsapp(contact, msg)
    message_var.set("")  # limpiar campo para siguiente mensaje

# UI
root = tk.Tk()
root.title("ENDEL-bot:- WhatsApp Desktop")
root.geometry("450x250")

contact_var = tk.StringVar()
message_var = tk.StringVar()

tk.Label(root, text="Contacto (opcional):").pack()
tk.Entry(root, textvariable=contact_var, width=40).pack()

tk.Label(root, text="Mensaje:").pack()
msg_entry = tk.Entry(root, textvariable=message_var, width=40)
msg_entry.pack()
msg_entry.bind("<Return>", on_send)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Enviar", command=on_send).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Calibrar búsqueda", command=calibrate_search).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Calibrar mensaje", command=calibrate_message).grid(row=0, column=2, padx=6)

tk.Label(root, text=f"Prefijo automático: {PREFIX}<texto>").pack(pady=10)

root.mainloop()
