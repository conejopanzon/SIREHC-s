# gui/app_window.py
import customtkinter as ctk
from core import database as db 
from services import ia_service 
import json                     

class App(ctk.CTk):
    def __init__(self, user_role):
        super().__init__()
        
        self.user_role = user_role
        self.title("Sistema de Gestión Clínica")
        self.geometry("1100x700")

        self.configure(fg_color="#F5F5F5")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.SPECIALTY_LIST = [
            'Médico General', 'Cardiología', 'Dermatología', 'Gastroenterología',
            'Neurólogo', 'Traumatólogo', 'Cirujano', 'Pediatra', 'Ginecólogo',
            'Oftalmólogo', 'Urólogo', 'Otorrinolaringólogo'
        ]

        self.load_doctors_list() 

        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#3B71CA")
        self.nav_frame.grid(row=0, column=0, sticky="nsew")

        self.label = ctk.CTkLabel(self.nav_frame, text=f"Rol: {self.user_role.capitalize()}",
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  text_color="#FFFFFF") 
        self.label.pack(pady=20, padx=20)

        nav_button_style = {
            "fg_color": "#FFFFFF",
            "text_color": "#3B71CA",
            "hover_color": "#EAEAEA"
        }
        
        self.btn_search = ctk.CTkButton(self.nav_frame, text="Buscar Paciente", command=self.show_search_frame, **nav_button_style)
        self.btn_search.pack(pady=10, padx=20, fill="x")
        
        self.btn_register = ctk.CTkButton(self.nav_frame, text="Registrar Paciente", command=self.show_register_frame, **nav_button_style)
        self.btn_register.pack(pady=10, padx=20, fill="x")

        self.btn_manual_cita = ctk.CTkButton(self.nav_frame, text="Agendar Cita Manual", command=self.show_manual_cita_frame, **nav_button_style)
        self.btn_manual_cita.pack(pady=10, padx=20, fill="x")

        self.btn_manage_citas = ctk.CTkButton(self.nav_frame, text="Gestionar Citas", command=self.show_citas_frame, **nav_button_style)
        self.btn_manage_citas.pack(pady=10, padx=20, fill="x")
        
        self.btn_manage_doctors = ctk.CTkButton(self.nav_frame, text="Gestionar Doctores", command=self.show_doctors_frame, **nav_button_style)
        self.btn_manage_doctors.pack(pady=10, padx=20, fill="x")

        self.btn_ia = ctk.CTkButton(self.nav_frame, text="Agendar Cita (IA)", command=self.show_ia_frame, **nav_button_style)
        self.btn_ia.pack(pady=10, padx=20, fill="x")

        if self.user_role == 'admin':
            self.btn_admin = ctk.CTkButton(self.nav_frame, text="Crear Usuarios", command=self.show_admin_frame, **nav_button_style)
            self.btn_admin.pack(pady=(10, 10), padx=20, fill="x") 

        self.main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.search_frame = self.create_search_frame()
        self.register_frame = self.create_register_frame()
        self.ia_frame = self.create_ia_frame()
        self.citas_frame = self.create_citas_frame() 
        self.doctors_frame = self.create_doctors_frame() 
        self.manual_cita_frame = self.create_manual_cita_frame() 
        self.admin_frame = self.create_admin_frame() if self.user_role == 'admin' else None

        self.show_search_frame() 

    # --- Funciones para MOSTRAR frames ---
    def hide_all_frames(self):
        self.search_frame.grid_forget()
        self.register_frame.grid_forget()
        self.ia_frame.grid_forget()
        self.citas_frame.grid_forget() 
        self.doctors_frame.grid_forget() 
        self.manual_cita_frame.grid_forget() 
        if self.admin_frame: self.admin_frame.grid_forget()

    def show_search_frame(self):
        self.hide_all_frames()
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.load_recent_appointments()

    def show_register_frame(self):
        self.hide_all_frames()
        self.register_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
    def show_admin_frame(self):
        self.hide_all_frames()
        if self.admin_frame:
            self.admin_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_ia_frame(self):
        self.hide_all_frames()
        self.ia_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_citas_frame(self):
        self.hide_all_frames()
        self.citas_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.refresh_citas_list() 

    def show_doctors_frame(self):
        self.hide_all_frames()
        self.doctors_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.refresh_doctors_list()

    def show_manual_cita_frame(self):
        self.hide_all_frames()
        self.manual_cita_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        for widget in self.manual_cita_search_results.winfo_children():
            widget.destroy()

    # --- Funciones para CREAR frames ---
    
    def create_search_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        search_bar_frame = ctk.CTkFrame(frame, fg_color="transparent")
        search_bar_frame.pack(pady=10, fill="x")

        ctk.CTkLabel(search_bar_frame, text="Buscar Paciente", font=ctk.CTkFont(size=20), text_color="#333333").pack(side="left", padx=(0, 20))
        self.search_entry = ctk.CTkEntry(search_bar_frame, placeholder_text="Buscar por nombre...", width=300)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(search_bar_frame, text="Buscar", command=self.perform_search, fg_color="#3B71CA", hover_color="#5A90E1").pack(side="left")
        
        self.search_results_label = ctk.CTkLabel(frame, text="Citas Recientes", font=ctk.CTkFont(size=16, weight="bold"), text_color="#333333")
        self.search_results_label.pack(pady=(10, 5), anchor="w")
        
        self.results_frame = ctk.CTkScrollableFrame(frame, fg_color="#F5F5F5")
        self.results_frame.pack(pady=0, fill="both", expand=True)
        
        return frame

    # --- MODIFICADO: create_register_frame ---
    def create_register_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        ctk.CTkLabel(frame, text="Registrar Nuevo Paciente", font=ctk.CTkFont(size=20), text_color="#333333").pack(pady=10)

        # Frame para DNI y Verificación
        dni_frame = ctk.CTkFrame(frame, fg_color="transparent")
        dni_frame.pack(pady=5, padx=50, fill="x")
        self.reg_dni = ctk.CTkEntry(dni_frame, placeholder_text="DNI (Obligatorio)")
        self.reg_dni.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # --- NUEVO: Botón de Verificación (Simulado) ---
        self.verify_dni_button = ctk.CTkButton(dni_frame, text="Verificar DNI (Simulado)", command=self._simulate_dni_check, fg_color="#5DADE2", hover_color="#8DC6E9")
        self.verify_dni_button.pack(side="left")

        # Frame para datos personales
        personal_frame = ctk.CTkFrame(frame, fg_color="transparent")
        personal_frame.pack(pady=5, padx=50, fill="x")
        self.reg_name = ctk.CTkEntry(personal_frame, placeholder_text="Nombre Completo")
        self.reg_name.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.reg_age = ctk.CTkEntry(personal_frame, placeholder_text="Edad", width=120)
        self.reg_age.pack(side="left")

        # Frame para datos médicos
        medical_frame = ctk.CTkFrame(frame, fg_color="transparent")
        medical_frame.pack(pady=5, padx=50, fill="x")
        self.reg_height = ctk.CTkEntry(medical_frame, placeholder_text="Altura (ej. 1.70)")
        self.reg_height.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.reg_weight = ctk.CTkEntry(medical_frame, placeholder_text="Peso (kg)")
        self.reg_weight.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.reg_blood_type = ctk.CTkComboBox(medical_frame, values=["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "No sabe"], width=140)
        self.reg_blood_type.set("Tipo de Sangre")
        self.reg_blood_type.pack(side="left")

        # Frame para contacto
        contact_frame = ctk.CTkFrame(frame, fg_color="transparent")
        contact_frame.pack(pady=5, padx=50, fill="x")
        self.reg_phone = ctk.CTkEntry(contact_frame, placeholder_text="Teléfono (Opcional)")
        self.reg_phone.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.reg_email = ctk.CTkEntry(contact_frame, placeholder_text="Email (Opcional)")
        self.reg_email.pack(side="left", fill="x", expand=True)
        
        self.reg_status_label = ctk.CTkLabel(frame, text="", text_color="green")
        self.reg_status_label.pack(pady=10)

        ctk.CTkButton(frame, text="Guardar Paciente", command=self.save_patient, fg_color="#4CAF50", hover_color="#81C784").pack(pady=20)

        return frame

    def create_admin_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(frame, text="Crear Nuevo Usuario", font=ctk.CTkFont(size=20), text_color="#333333").pack(pady=10)
        
        self.admin_user = ctk.CTkEntry(frame, placeholder_text="Nuevo Username")
        self.admin_user.pack(pady=5, padx=50, fill="x")
        self.admin_pass = ctk.CTkEntry(frame, placeholder_text="Nueva Password", show="*")
        self.admin_pass.pack(pady=5, padx=50, fill="x")
        self.admin_role = ctk.CTkComboBox(frame, values=["doctor", "recepcionista", "admin"])
        self.admin_role.set("Seleccionar rol")
        self.admin_role.pack(pady=5, padx=50, fill="x")
        self.admin_status_label = ctk.CTkLabel(frame, text="", text_color="green")
        self.admin_status_label.pack(pady=10)

        ctk.CTkButton(frame, text="Crear Usuario", command=self.save_new_user, fg_color="#3B71CA", hover_color="#5A90E1").pack(pady=20)
        
        return frame

    def create_ia_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        ctk.CTkLabel(frame, text="Agendar Cita con IA", font=ctk.CTkFont(size=20), text_color="#333333").pack(pady=10)
        ctk.CTkLabel(frame, text="Escribe tu petición (ej: 'Soy Cristhian Machaca, DNI 123... y quiero cita...')", text_color="#555555").pack(pady=5)

        self.ia_entry = ctk.CTkEntry(frame, placeholder_text="Tu petición aquí...", width=500)
        self.ia_entry.pack(pady=10)
        self.ia_button = ctk.CTkButton(frame, text="Procesar con IA", command=self.procesar_con_ia, fg_color="#3B71CA", hover_color="#5A90E1")
        self.ia_button.pack(pady=10)
        
        # --- MODIFICADO: Ventana emergente en lugar de textbox ---
        
        def refresh_data():
            """Limpia el entry de IA al cambiar de pestaña."""
            self.ia_entry.delete(0, 'end')
        
        frame.refresh_data = refresh_data
        
        return frame

    def create_citas_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="Lista de Todas las Citas", font=ctk.CTkFont(size=20), text_color="#333333").pack(side="left")
        ctk.CTkButton(header_frame, text="Actualizar", command=self.refresh_citas_list, fg_color="#5DADE2", hover_color="#8DC6E9").pack(side="right")
        
        self.citas_scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="#F5F5F5")
        self.citas_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        return frame

    def create_doctors_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="Lista de Doctores", font=ctk.CTkFont(size=20), text_color="#333333").pack(side="left")
        
        ctk.CTkButton(header_frame, text="Añadir Doctor", command=self.show_add_doctor_window, 
                      fg_color="#4CAF50", hover_color="#81C784").pack(side="right", padx=10)
        
        ctk.CTkButton(header_frame, text="Actualizar", command=self.refresh_doctors_list, 
                      fg_color="#5DADE2", hover_color="#8DC6E9").pack(side="right")
        
        self.doctors_scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="#F5F5F5")
        self.doctors_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        return frame

    def create_manual_cita_frame(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        ctk.CTkLabel(frame, text="Agendar Cita Manual", font=ctk.CTkFont(size=20), text_color="#333333").pack(pady=10)
        ctk.CTkLabel(frame, text="Paso 1: Busque y seleccione al paciente", font=ctk.CTkFont(size=16), text_color="#555555").pack(pady=(0, 10))

        search_bar_frame = ctk.CTkFrame(frame, fg_color="transparent")
        search_bar_frame.pack(pady=10, fill="x")

        self.manual_cita_search_entry = ctk.CTkEntry(search_bar_frame, placeholder_text="Buscar por nombre o DNI...", width=300)
        self.manual_cita_search_entry.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(search_bar_frame, text="Buscar Paciente", command=self.perform_manual_patient_search, fg_color="#3B71CA", hover_color="#5A90E1").pack(side="left")
        
        self.manual_cita_search_results = ctk.CTkScrollableFrame(frame, fg_color="#F5F5F5")
        self.manual_cita_search_results.pack(pady=10, fill="both", expand=True)
        
        return frame

    # --- Lógica de Carga de Datos ---
    def load_doctors_list(self):
        self.doctors_list = db.get_all_doctors()
        self.doctors_map = {}
        for (doc_id, name, specialty) in self.doctors_list:
            display_name = f"{name} ({specialty})"
            self.doctors_map[display_name] = doc_id
        
        self.doctors_map_reverse = {v: k for k, v in self.doctors_map.items()}

    # --- Lógica de Funciones ---

    # --- NUEVA FUNCIÓN ---
    def _simulate_dni_check(self):
        dni = self.reg_dni.get()
        if not dni:
            self.reg_status_label.configure(text="Por favor, ingrese un DNI para verificar.", text_color="red")
            return
        
        # Simulación de autocompletado
        self.reg_name.delete(0, "end")
        self.reg_name.insert(0, "Juan Pérez (Simulado RENIEC)")
        self.reg_age.delete(0, "end")
        self.reg_age.insert(0, "30")
        
        self.reg_status_label.configure(text="Datos de DNI (simulados) cargados. Complete el resto.", text_color="green")

    # --- MODIFICADO: save_patient ---
    def save_patient(self):
        name = self.reg_name.get()
        dni = self.reg_dni.get()
        phone = self.reg_phone.get()
        email = self.reg_email.get()
        age_str = self.reg_age.get()
        height_str = self.reg_height.get()
        weight_str = self.reg_weight.get()
        blood_type = self.reg_blood_type.get()

        if not name or not dni:
            self.reg_status_label.configure(text="Nombre Completo y DNI son obligatorios.", text_color="red")
            return

        # Validación de números
        try:
            age = int(age_str) if age_str else None
            height = float(height_str) if height_str else None
            weight = float(weight_str) if weight_str else None
        except ValueError:
            self.reg_status_label.configure(text="Error: Edad, Altura y Peso deben ser números.", text_color="red")
            return

        if blood_type == "Tipo de Sangre":
            blood_type = "No sabe"

        if db.register_patient(name, dni, phone, email, age, height, weight, blood_type):
            self.reg_status_label.configure(text=f"Paciente {name} guardado con éxito.", text_color="green")
            # Limpiar campos
            self.reg_name.delete(0, 'end'); self.reg_dni.delete(0, 'end'); self.reg_phone.delete(0, 'end')
            self.reg_email.delete(0, 'end'); self.reg_age.delete(0, 'end'); self.reg_height.delete(0, 'end')
            self.reg_weight.delete(0, 'end'); self.reg_blood_type.set("Tipo de Sangre")
        else:
            self.reg_status_label.configure(text=f"Error: El DNI '{dni}' ya existe.", text_color="red")

    def save_new_user(self):
        user = self.admin_user.get()
        pwd = self.admin_pass.get()
        role = self.admin_role.get()

        if user and pwd and role != "Seleccionar rol":
            if db.create_user(user, pwd, role):
                self.admin_status_label.configure(text=f"Usuario {user} creado.", text_color="green")
                self.admin_user.delete(0, 'end'); self.admin_pass.delete(0, 'end')
            else:
                self.admin_status_label.configure(text=f"Error: Usuario {user} ya existe.", text_color="red")
        else:
            self.admin_status_label.configure(text="Todos los campos son obligatorios.", text_color="red")

    def perform_search(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        query = self.search_entry.get()
        
        if not query:
            self.load_recent_appointments() 
            return
        
        self.search_results_label.configure(text="Resultados de Búsqueda") 
        
        results = db.search_patient_by_name(query)
        
        if not results:
            ctk.CTkLabel(self.results_frame, text="No se encontraron pacientes.", text_color="#555555").pack(pady=10)
            return
            
        for patient in results:
            patient_id, full_name, dni = patient
            
            result_entry = ctk.CTkFrame(self.results_frame, fg_color="#F0F0F0", corner_radius=5)
            result_entry.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(result_entry, text=f"{full_name} (DNI: {dni if dni else 'N/A'})", text_color="#333333").pack(side="left", padx=10)
            
            ctk.CTkButton(result_entry, text="Editar", 
                          width=80,
                          fg_color="#f0ad4e", hover_color="#f1c40f", 
                          command=lambda pid=patient_id: self.show_edit_patient_window(pid)
                         ).pack(side="right", padx=(5, 5))
            
            ctk.CTkButton(result_entry, text="Ver Historial", 
                          width=100,
                          fg_color="#5DADE2", hover_color="#8DC6E9", 
                          command=lambda pid=patient_id: self.show_patient_history(pid)
                         ).pack(side="right", padx=(0, 10))

    def show_patient_history(self, patient_id, ia_data=None):
        history_window = ctk.CTkToplevel(self)
        history_window.title("Registrar Nueva Cita / Emergencia")
        history_window.geometry("900x600")
        history_window.grab_set() 
        history_window.configure(fg_color="#FFFFFF")

        emergency_frame = ctk.CTkFrame(history_window, fg_color="transparent")
        emergency_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(emergency_frame, text="REGISTRAR CITA / EMERGENCIA", font=ctk.CTkFont(size=16), text_color="#333333").pack(pady=5)
        
        ctk.CTkLabel(emergency_frame, text="Doctor", text_color="#555555").pack(anchor="w", padx=10)
        doctor_combobox = ctk.CTkComboBox(emergency_frame)
        doctor_combobox.pack(pady=(0, 10), padx=10, fill="x")

        ctk.CTkLabel(emergency_frame, text="Razón de Consulta (Síntomas)", text_color="#555555").pack(anchor="w", padx=10)
        reason_entry = ctk.CTkEntry(emergency_frame, placeholder_text="Razón de Consulta")
        reason_entry.pack(pady=(0, 10), padx=10, fill="x")

        ctk.CTkLabel(emergency_frame, text="Posible Diagnóstico", text_color="#555555").pack(anchor="w", padx=10)
        diag_entry = ctk.CTkEntry(emergency_frame, placeholder_text="Diagnóstico (ej. Migraña)")
        diag_entry.pack(pady=(0, 10), padx=10, fill="x")

        blood_entry = ctk.CTkEntry(emergency_frame, placeholder_text="Tipo de Sangre")
        blood_entry.pack(pady=2, padx=10, side="left", expand=True, fill="x")
        oncology_entry = ctk.CTkEntry(emergency_frame, placeholder_text="Enf. Oncológica (si aplica)")
        oncology_entry.pack(pady=2, padx=10, side="left", expand=True, fill="x")
        
        filtered_doctors_map = self.doctors_map
        
        if ia_data and ia_data.get('especialista_recomendado') and ia_data.get('especialista_recomendado') != 'N/A':
            specialty = ia_data.get('especialista_recomendado')
            filtered_doctors_map = {}
            for (doc_id, name, spec) in self.doctors_list:
                if spec == specialty:
                    display_name = f"{name} ({spec})"
                    filtered_doctors_map[display_name] = doc_id
            
            if not filtered_doctors_map: 
                filtered_doctors_map = self.doctors_map

        doctor_combobox.configure(values=list(filtered_doctors_map.keys()))
        if filtered_doctors_map:
             doctor_combobox.set(list(filtered_doctors_map.keys())[0]) 

        if ia_data:
            if ia_data.get('motivo') and ia_data.get('motivo') != 'N/A':
                reason_entry.insert(0, ia_data.get('motivo'))
            if ia_data.get('posible_enfermedad') and ia_data.get('posible_enfermedad') != 'N/A':
                diag_entry.insert(0, ia_data.get('posible_enfermedad'))
            if ia_data.get('doctor') and ia_data.get('doctor') != 'N/A':
                 doc_name_ai = ia_data.get('doctor')
                 for display_name in self.doctors_map.keys():
                     if doc_name_ai in display_name:
                         doctor_combobox.set(display_name)
                         break
        
        def save_emergency():
            selected_doctor_name = doctor_combobox.get()
            
            db.add_emergency_record(
                patient_id, 
                selected_doctor_name, 
                reason_entry.get(), 
                diag_entry.get(),
                blood_entry.get(), 
                oncology_entry.get()
            )
            print("Cita/Emergencia guardada")
            history_window.destroy() 

        ctk.CTkButton(history_window, text="Guardar Registro", command=save_emergency, 
                      fg_color="#471DE1", hover_color="#1672E3").pack(pady=10, fill="x", padx=10)

        ctk.CTkLabel(history_window, text="Historial Pasado", font=ctk.CTkFont(size=16), text_color="#333333").pack(pady=10)
        history_scroll_frame = ctk.CTkScrollableFrame(history_window, fg_color="#FFFFFF")
        history_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        history_data = db.get_patient_history(patient_id)
        if not history_data:
            ctk.CTkLabel(history_scroll_frame, text="El paciente no tiene historial.", text_color="#555555").pack()
            return
        for record in history_data:
            (id, patient_id, date, doctor, reason, diag, is_emergency, blood, oncology) = record
            color = "#FADBD8" if is_emergency else "#F0F0F0"
            record_frame = ctk.CTkFrame(history_scroll_frame, fg_color=color, corner_radius=5)
            record_frame.pack(fill="x", pady=4, padx=4)
            emerg_text = "EMERGENCIA" if is_emergency else "Cita Regular"
            label_text = f"[{emerg_text}] {date} - {doctor} - Motivo: {reason}"
            ctk.CTkLabel(record_frame, text=label_text, text_color="#333333").pack(anchor="w", padx=10, pady=10)

    # --- MODIFICADO: show_edit_patient_window ---
    def show_edit_patient_window(self, patient_id):
        patient_data = db.get_patient_by_id(patient_id)
        if not patient_data: return
            
        (pid, full_name, dni, phone, email, age, height, weight, blood_type) = patient_data
        
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Paciente")
        edit_window.geometry("500x550") # Más alto
        edit_window.grab_set() 
        edit_window.configure(fg_color="#FFFFFF")

        ctk.CTkLabel(edit_window, text=f"Editando a: {full_name}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333").pack(pady=15)
        
        form_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        form_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(form_frame, text="Nombre Completo", text_color="#555555").pack(anchor="w")
        edit_name_entry = ctk.CTkEntry(form_frame, width=400)
        edit_name_entry.insert(0, full_name if full_name else "")
        edit_name_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="DNI", text_color="#555555").pack(anchor="w")
        edit_dni_entry = ctk.CTkEntry(form_frame, width=400)
        edit_dni_entry.insert(0, dni if dni else "")
        edit_dni_entry.pack(pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Edad", text_color="#555555").pack(anchor="w")
        edit_age_entry = ctk.CTkEntry(form_frame, width=400)
        edit_age_entry.insert(0, str(age) if age else "")
        edit_age_entry.pack(pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Altura (m)", text_color="#555555").pack(anchor="w")
        edit_height_entry = ctk.CTkEntry(form_frame, width=400)
        edit_height_entry.insert(0, str(height) if height else "")
        edit_height_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Peso (kg)", text_color="#555555").pack(anchor="w")
        edit_weight_entry = ctk.CTkEntry(form_frame, width=400)
        edit_weight_entry.insert(0, str(weight) if weight else "")
        edit_weight_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Tipo de Sangre", text_color="#555555").pack(anchor="w")
        edit_blood_combo = ctk.CTkComboBox(form_frame, width=400, values=["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "No sabe"])
        edit_blood_combo.set(blood_type if blood_type else "No sabe")
        edit_blood_combo.pack(pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Teléfono", text_color="#555555").pack(anchor="w")
        edit_phone_entry = ctk.CTkEntry(form_frame, width=400)
        edit_phone_entry.insert(0, phone if phone else "")
        edit_phone_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Email", text_color="#555555").pack(anchor="w")
        edit_email_entry = ctk.CTkEntry(form_frame, width=400)
        edit_email_entry.insert(0, email if email else "")
        edit_email_entry.pack(pady=(0, 10))
        
        status_label = ctk.CTkLabel(edit_window, text="", text_color="red")
        status_label.pack(pady=5)

        def save_changes():
            new_name = edit_name_entry.get()
            new_dni = edit_dni_entry.get()
            new_phone = edit_phone_entry.get()
            new_email = edit_email_entry.get()
            new_age_str = edit_age_entry.get()
            new_height_str = edit_height_entry.get()
            new_weight_str = edit_weight_entry.get()
            new_blood = edit_blood_combo.get()

            if not new_name:
                status_label.configure(text="El nombre no puede estar vacío.")
                return
            
            try:
                new_age = int(new_age_str) if new_age_str else None
                new_height = float(new_height_str) if new_height_str else None
                new_weight = float(new_weight_str) if new_weight_str else None
            except ValueError:
                status_label.configure(text="Error: Edad, Altura y Peso deben ser números.", text_color="red")
                return
                
            if db.update_patient_details(patient_id, new_name, new_dni, new_phone, new_email, new_age, new_height, new_weight, new_blood):
                print("Paciente actualizado con éxito.")
                edit_window.destroy()
                self.perform_search() 
            else:
                status_label.configure(text=f"Error: El DNI '{new_dni}' ya existe.")
        
        ctk.CTkButton(edit_window, text="Guardar Cambios", 
                      command=save_changes,
                      fg_color="#4CAF50", hover_color="#81C784"
                     ).pack(pady=10)

    # --- Lógica de IA (MODIFICADA) ---
    def procesar_con_ia(self):
        prompt = self.ia_entry.get()
        if not prompt: return

        self.ia_button.configure(text="Procesando...", state="disabled")
        self.update_idletasks() 
        
        respuesta_json_str = ia_service.obtener_cita_ia(prompt)

        self.ia_button.configure(text="Procesar con IA", state="normal")
        
        # --- NUEVA VENTANA EMERGENTE ---
        popup = ctk.CTkToplevel(self)
        popup.title("Resultado del Análisis de IA")
        popup.geometry("600x400")
        popup.grab_set()
        
        popup_textbox = ctk.CTkTextbox(popup, text_color="#333333", wrap="word")
        popup_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        # --- FIN DE VENTANA EMERGENTE ---
        
        try:
            datos = json.loads(respuesta_json_str)
            
            if "error" in datos:
                popup_textbox.insert("1.0", f"Error de la IA: {datos['error']}")
                popup_textbox.configure(state="disabled")
                return

            # --- Formateo de texto limpio ---
            paciente = datos.get('paciente', 'N/A')
            motivo = datos.get('motivo', 'N/A')
            enfermedad = datos.get('posible_enfermedad', 'N/A')
            especialista = datos.get('especialista_recomendado', 'N/A')
            dni_ia = datos.get('dni', 'N/A')

            resumen_texto = f"Análisis de IA Completado:\n"
            resumen_texto += f"----------------------------------\n"
            resumen_texto += f"Paciente Detectado: {paciente}\n"
            resumen_texto += f"DNI Detectado: {dni_ia}\n"
            resumen_texto += f"Síntomas/Motivo: {motivo}\n"
            resumen_texto += f"Posible Condición: {enfermedad}\n"
            resumen_texto += f"Especialista Recomendado: {especialista}\n"
            resumen_texto += f"----------------------------------\n\n"
            
            popup_textbox.insert("1.0", resumen_texto)
            # --- Fin de texto limpio ---

            popup_textbox.insert("end", "Estado de la Automatización:\n")
            
            if not paciente or paciente == 'N/A':
                popup_textbox.insert("end", "IA no detectó un nombre de paciente. No se tomará ninguna acción automática.")
                popup_textbox.configure(state="disabled")
                return

            popup_textbox.insert("end", f"Buscando paciente: '{paciente}'...\n")
            search_results = db.search_patient_by_name(paciente)
            
            patient_id_to_open = None

            if len(search_results) == 1:
                patient_id_to_open = search_results[0][0] 
                full_name = search_results[0][1] 
                popup_textbox.insert("end", f"¡Paciente encontrado!: {full_name}\nAbriendo historial...")
            
            elif len(search_results) > 1:
                popup_textbox.insert("end", "Se encontraron varios pacientes. Abriendo el historial del primero...")
                patient_id_to_open = search_results[0][0] 
            
            else:
                popup_textbox.insert("end", "Paciente no encontrado. Registrando nuevo paciente...\n")
                
                patient_dni = datos.get('dni')
                patient_phone = datos.get('phone')
                # Obtener nuevos datos de la IA
                age = datos.get('age') if datos.get('age') != 'N/A' else None
                height = datos.get('height') if datos.get('height') != 'N/A' else None
                weight = datos.get('weight') if datos.get('weight') != 'N/A' else None
                blood_type = datos.get('blood_type') if datos.get('blood_type') != 'N/A' else None

                new_patient_id = db.register_patient(
                    full_name=paciente,
                    dni=patient_dni,
                    phone=patient_phone,
                    email=None,
                    age=age,
                    height=height,
                    weight=weight,
                    blood_type=blood_type
                )
                
                if new_patient_id:
                    popup_textbox.insert("end", f"¡Paciente '{paciente}' registrado con ID: {new_patient_id}!\n")
                    popup_textbox.insert("end", "Abriendo historial y autorrellenando datos...")
                    patient_id_to_open = new_patient_id
                else:
                    popup_textbox.insert("end", f"Error al registrar al nuevo paciente. ¿El DNI '{patient_dni}' ya existe?")
            
            if patient_id_to_open:
                popup.after(1000, popup.destroy) # Cerrar popup
                self.show_patient_history(patient_id_to_open, ia_data=datos)
            
        except json.JSONDecodeError:
            popup_textbox.insert("1.0", "Error: La respuesta de la IA no fue un JSON válido.\n")
            popup_textbox.insert("end", respuesta_json_str)
            
        popup_textbox.configure(state="disabled")

    # --- Lógica de Gestión de Citas ---
    
    def refresh_citas_list(self):
        for widget in self.citas_scroll_frame.winfo_children():
            widget.destroy()
            
        citas = db.get_all_appointments_with_details()
        
        if not citas:
            ctk.CTkLabel(self.citas_scroll_frame, text="No hay citas registradas.", text_color="#555555").pack(pady=10)
            return
            
        for cita in citas:
            (cita_id, patient_name, date, doctor, reason, diagnosis) = cita
            
            if not patient_name: patient_name = "Paciente Eliminado"
            
            entry_frame = ctk.CTkFrame(self.citas_scroll_frame, fg_color="#F0F0F0", corner_radius=5)
            entry_frame.pack(fill="x", pady=5, padx=5)
            
            info_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
            info_frame.pack(side="left", padx=10, pady=5)

            ctk.CTkLabel(info_frame, text=f"{patient_name} - {doctor}", font=ctk.CTkFont(weight="bold"), text_color="#333333").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Fecha: {date}", text_color="#555555").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Motivo: {reason}", text_color="#555555").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Posible Diag.: {diagnosis if diagnosis else 'N/A'}", text_color="#555555").pack(anchor="w")

            button_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
            button_frame.pack(side="right", padx=10)

            ctk.CTkButton(button_frame, text="Editar", 
                          width=80,
                          fg_color="#f0ad4e", hover_color="#f1c40f",
                          command=lambda cid=cita_id: self.show_edit_appointment_window(cid)
                         ).pack(pady=(5,5))
            
            ctk.CTkButton(button_frame, text="Eliminar", 
                          width=80,
                          fg_color="#E74C3C", hover_color="#F1948A",
                          command=lambda cid=cita_id: self.delete_cita_callback(cid)
                         ).pack(pady=(5,5))
            
    def delete_cita_callback(self, appointment_id):
        if db.delete_appointment(appointment_id):
            self.refresh_citas_list() 
            self.load_recent_appointments() 
        else:
            print("Error al eliminar.")

    def show_edit_appointment_window(self, appointment_id):
        cita_data = db.get_appointment_by_id(appointment_id)
        if not cita_data: return
            
        (cid, app_date, doctor_name, reason, diagnosis) = cita_data
        
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Cita")
        edit_window.geometry("500x450")
        edit_window.grab_set() 
        edit_window.configure(fg_color="#FFFFFF")

        ctk.CTkLabel(edit_window, text=f"Editando Cita ID: {cid}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333").pack(pady=15)
        
        form_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        form_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(form_frame, text="Fecha y Hora (Formato: YYYY-MM-DD HH:MM)", text_color="#555555").pack(anchor="w")
        edit_date_entry = ctk.CTkEntry(form_frame, width=400)
        edit_date_entry.insert(0, app_date if app_date else "")
        edit_date_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Doctor", text_color="#555555").pack(anchor="w")
        edit_doctor_combo = ctk.CTkComboBox(form_frame, width=400, values=list(self.doctors_map.keys()))
        if doctor_name in self.doctors_map.keys():
            edit_doctor_combo.set(doctor_name)
        elif self.doctors_map:
            edit_doctor_combo.set(list(self.doctors_map.keys())[0]) 
        edit_doctor_combo.pack(pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Razón de Consulta (Síntomas)", text_color="#555555").pack(anchor="w")
        edit_reason_entry = ctk.CTkEntry(form_frame, width=400)
        edit_reason_entry.insert(0, reason if reason else "")
        edit_reason_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Diagnóstico", text_color="#555555").pack(anchor="w")
        edit_diag_entry = ctk.CTkEntry(form_frame, width=400)
        edit_diag_entry.insert(0, diagnosis if diagnosis else "")
        edit_diag_entry.pack(pady=(0, 10))
        
        status_label = ctk.CTkLabel(edit_window, text="", text_color="red")
        status_label.pack(pady=5)

        def save_cita_changes():
            new_date = edit_date_entry.get()
            new_doctor = edit_doctor_combo.get()
            new_reason = edit_reason_entry.get()
            new_diag = edit_diag_entry.get()

            if not new_date or not new_doctor:
                status_label.configure(text="Fecha y Doctor son obligatorios.")
                return
                
            if db.update_appointment(appointment_id, new_date, new_doctor, new_reason, new_diag):
                print("Cita actualizada con éxito.")
                edit_window.destroy()
                self.refresh_citas_list() 
                self.load_recent_appointments()
            else:
                status_label.configure(text="Error al guardar en la base de datos.")
        
        ctk.CTkButton(edit_window, text="Guardar Cambios", 
                      command=save_cita_changes,
                      fg_color="#4CAF50", hover_color="#81C784"
                     ).pack(pady=10)

    def load_recent_appointments(self):
        self.search_results_label.configure(text="Citas Recientes")
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        citas = db.get_recent_appointments(limit=5)
        
        if not citas:
            ctk.CTkLabel(self.results_frame, text="No hay citas registradas.", text_color="#555555").pack(pady=10)
            return
            
        for cita in citas:
            (cita_id, patient_name, date, doctor, reason, diagnosis) = cita
            
            if not patient_name: patient_name = "Paciente Eliminado"
            
            entry_frame = ctk.CTkFrame(self.results_frame, fg_color="#F0F0F0", corner_radius=5)
            entry_frame.pack(fill="x", pady=5, padx=5)
            
            info_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
            info_frame.pack(side="left", padx=10, pady=5)

            ctk.CTkLabel(info_frame, text=f"{patient_name} - {doctor}", font=ctk.CTkFont(weight="bold"), text_color="#333333").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Fecha: {date}", text_color="#555555").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Motivo: {reason}", text_color="#555555").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Posible Diag.: {diagnosis if diagnosis else 'N/A'}", text_color="#555555").pack(anchor="w")

            button_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
            button_frame.pack(side="right", padx=10)

            ctk.CTkButton(button_frame, text="Editar", 
                          width=80,
                          fg_color="#f0ad4e", hover_color="#f1c40f",
                          command=lambda cid=cita_id: self.show_edit_appointment_window(cid)
                         ).pack(pady=(5,5))
            
            ctk.CTkButton(button_frame, text="Eliminar", 
                          width=80,
                          fg_color="#E74C3C", hover_color="#F1948A",
                          command=lambda cid=cita_id: self.delete_cita_callback(cid)
                         ).pack(pady=(5,5))

    def refresh_doctors_list(self):
        for widget in self.doctors_scroll_frame.winfo_children():
            widget.destroy()
            
        self.load_doctors_list() 
        
        if not self.doctors_list:
            ctk.CTkLabel(self.doctors_scroll_frame, text="No hay doctores registrados.", text_color="#555555").pack(pady=10)
            return
            
        current_specialty = ""
        for (doc_id, name, specialty) in self.doctors_list:
            
            if specialty != current_specialty:
                ctk.CTkLabel(self.doctors_scroll_frame, text=specialty, font=ctk.CTkFont(size=16, weight="bold"), text_color="#3B71CA").pack(fill="x", pady=(10, 2), padx=10)
                current_specialty = specialty

            entry_frame = ctk.CTkFrame(self.doctors_scroll_frame, fg_color="#F0F0F0", corner_radius=5)
            entry_frame.pack(fill="x", pady=2, padx=10)
            
            ctk.CTkLabel(entry_frame, text=name, text_color="#333333").pack(side="left", padx=10, pady=10)

    def show_add_doctor_window(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Añadir Nuevo Doctor")
        add_window.geometry("400x300")
        add_window.grab_set() 
        add_window.configure(fg_color="#FFFFFF")

        ctk.CTkLabel(add_window, text="Añadir Nuevo Doctor", font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333").pack(pady=15)
        
        form_frame = ctk.CTkFrame(add_window, fg_color="transparent")
        form_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(form_frame, text="Nombre Completo", text_color="#555555").pack(anchor="w")
        name_entry = ctk.CTkEntry(form_frame, width=300)
        name_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Especialidad", text_color="#555555").pack(anchor="w")
        specialty_combo = ctk.CTkComboBox(form_frame, width=300, values=self.SPECIALTY_LIST)
        specialty_combo.set(self.SPECIALTY_LIST[0]) 
        specialty_combo.pack(pady=(0, 10))

        status_label = ctk.CTkLabel(add_window, text="", text_color="red")
        status_label.pack(pady=5)

        def save_doctor():
            name = name_entry.get()
            specialty = specialty_combo.get()

            if not name or not specialty:
                status_label.configure(text="Nombre y especialidad son obligatorios.")
                return
                
            if db.add_doctor(name, specialty):
                print("Doctor añadido con éxito.")
                add_window.destroy()
                self.refresh_doctors_list() 
            else:
                status_label.configure(text="Error al guardar en la base de datos.")
        
        ctk.CTkButton(add_window, text="Guardar Doctor", 
                      command=save_doctor,
                      fg_color="#4CAF50", hover_color="#81C784"
                     ).pack(pady=10)

    def perform_manual_patient_search(self):
        for widget in self.manual_cita_search_results.winfo_children():
            widget.destroy()

        query = self.manual_cita_search_entry.get()
        if not query: return
        
        results = db.search_patient_by_name(query)
        
        if not results:
            ctk.CTkLabel(self.manual_cita_search_results, text="No se encontraron pacientes.", text_color="#55555G").pack(pady=10)
            return
            
        for patient in results:
            patient_id, full_name, dni = patient
            
            result_entry = ctk.CTkFrame(self.manual_cita_search_results, fg_color="#F0F0F0", corner_radius=5)
            result_entry.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(result_entry, text=f"{full_name} (DNI: {dni if dni else 'N/A'})", text_color="#333333").pack(side="left", padx=10)
            
            ctk.CTkButton(result_entry, text="Agendar Cita", 
                          fg_color="#5DADE2", hover_color="#8DC6E9", 
                          command=lambda pid=patient_id: self.show_patient_history(pid, ia_data=None)
                         ).pack(side="right", padx=(0, 10))