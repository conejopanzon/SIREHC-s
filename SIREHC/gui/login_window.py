# gui/login_window.py
import customtkinter as ctk
from PIL import Image
import os
from core import database as db
from gui.app_window import App

class LoginWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión de Citas Médicas")
        self.geometry("900x550")
        self.resizable(False, False)
        
        # Centrar ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color="#FFFFFF")
        
        # ===== FRAME IZQUIERDO CON IMAGEN =====
        left_frame = ctk.CTkFrame(self, fg_color="#E8F4F8", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Cargar y mostrar imagen médica
        try:
            image_path = os.path.join(os.path.dirname(__file__), "assets", "medical_bg.png")
            if os.path.exists(image_path):
                medical_image = ctk.CTkImage(Image.open(image_path), size=(450, 550))
                image_label = ctk.CTkLabel(left_frame, image=medical_image, text="")
                image_label.image = medical_image  # Mantener referencia
                image_label.grid(row=0, column=0, sticky="nsew")
            else:
                # Mostrar placeholder si no existe imagen
                placeholder = ctk.CTkLabel(
                    left_frame,
                    text="🏥\n\nSistema de Citas\nMédicas",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#1F6E78"
                )
                placeholder.grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            placeholder = ctk.CTkLabel(
                left_frame,
                text="🏥\n\nSistema de Citas\nMédicas",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#1F6E78"
            )
            placeholder.grid(row=0, column=0, sticky="nsew")
        
        # ===== FRAME DERECHO CON FORMULARIO =====
        right_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Contenedor del formulario (centrado)
        form_container = ctk.CTkFrame(right_frame, fg_color="#FFFFFF")
        form_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        
        # Marco interior con padding
        inner_frame = ctk.CTkFrame(form_container, fg_color="#FFFFFF")
        inner_frame.pack(pady=40, padx=50, expand=True)
        
        # ===== ENCABEZADO =====
        header_frame = ctk.CTkFrame(inner_frame, fg_color="#FFFFFF")
        header_frame.pack(pady=(0, 30), fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Bienvenido",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1F6E78"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Ingrese sus credenciales para continuar",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # ===== CAMPOS DE ENTRADA =====
        # Usuario
        user_label = ctk.CTkLabel(
            inner_frame,
            text="Usuario",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        )
        user_label.pack(anchor="w", pady=(15, 5))
        
        self.user_entry = ctk.CTkEntry(
            inner_frame,
            placeholder_text="admin",
            width=300,
            height=40,
            border_width=1.5,
            border_color="#D0D0D0",
            fg_color="#F9F9F9"
        )
        self.user_entry.pack(pady=(0, 15), fill="x")
        
        # Contraseña
        pass_label = ctk.CTkLabel(
            inner_frame,
            text="Contraseña",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333"
        )
        pass_label.pack(anchor="w", pady=(0, 5))
        
        self.pass_entry = ctk.CTkEntry(
            inner_frame,
            placeholder_text="admin123",
            width=300,
            height=40,
            show="•",
            border_width=1.5,
            border_color="#D0D0D0",
            fg_color="#F9F9F9"
        )
        self.pass_entry.pack(pady=(0, 25), fill="x")
        
        # ===== BOTONES =====
        login_button = ctk.CTkButton(
            inner_frame,
            text="Iniciar Sesión",
            width=300,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1F6E78",
            hover_color="#155C64",
            text_color="#FFFFFF",
            command=self.attempt_login
        )
        login_button.pack(pady=(0, 12), fill="x")
        
        register_button = ctk.CTkButton(
            inner_frame,
            text="Crear Cuenta",
            width=300,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1.5,
            border_color="#1F6E78",
            text_color="#1F6E78",
            hover_color="#E8F4F8",
            command=self.show_message
        )
        register_button.pack(fill="x")
        
        # Mensaje de estado
        self.status_label = ctk.CTkLabel(
            inner_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#E74C3C"
        )
        self.status_label.pack(pady=(20, 0))
        
        # Permitir Enter para login
        self.bind("<Return>", lambda e: self.attempt_login())
        
        # Focus inicial en usuario
        self.user_entry.focus()

    def attempt_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            self.status_label.configure(text="Por favor completa todos los campos")
            return
        
        user_role = db.check_login(username, password)
        
        if user_role:
            print(f"Login exitoso como: {user_role}")
            self.destroy() 
            main_app = App(user_role=user_role)
            main_app.mainloop()
        else:
            self.status_label.configure(text="❌ Usuario o contraseña incorrectos")
            self.pass_entry.delete(0, ctk.END)
            self.user_entry.focus()
    
    def show_message(self):
        self.status_label.configure(text="✓ Función de registro disponible próximamente")