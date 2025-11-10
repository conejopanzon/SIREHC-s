# main.py
import customtkinter as ctk
from core import database as db
from gui.login_window import LoginWindow

# 1. Asegurarse que la DB esté inicializada
db.init_db()

# 2. --- CAMBIO DE TEMA ---
# Cambiamos el modo a "light" para un aspecto clínico
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
# --- FIN DE CAMBIO DE TEMA ---

# 3. Iniciar la aplicación
if __name__ == "__main__":
    login_app = LoginWindow()
    login_app.mainloop()