# core/database.py
import sqlite3

def _populate_doctors_table(cursor):
    """
    (Función interna) Rellena la tabla de doctores con datos de ejemplo.
    Se ejecuta solo si la tabla está vacía.
    """
    try:
        cursor.execute("SELECT COUNT(*) FROM doctors")
        if cursor.fetchone()[0] > 0:
            return 

        # --- LISTA COMPLETA DE DOCTORES DE EJEMPLO CON ESPECIALIDADES AMPLIADAS ---
        doctores = [
            # Médico General (General Practice)
            ('Dr. Juan Pérez', 'Médico General'),
            ('Dra. Ana García', 'Médico General'),
            
            # Especialidades del Corazón
            ('Dr. Luis Martínez', 'Cardiología'),
            ('Dra. María Rodríguez', 'Cardiología'),
            ('Dr. Ricardo Blanco', 'Cirugía Cardiovascular'),
            
            # Especialidades de la Piel
            ('Dr. Carlos Sánchez', 'Dermatología'),
            
            # Especialidades de Digestion y Nutrición
            ('Dra. Laura Gómez', 'Gastroenterología'),
            ('Dr. Miguel Torres', 'Endocrinología y Nutrición'),
            
            # Especialidades Neurológicas
            ('Dra. Sofía Díaz', 'Neurología'),
            ('Dr. Javier Ortiz', 'Neurocirugía'),
            ('Dra. Elena Flores', 'Psiquiatría'),
            
            # Otras Cirugías y Aparato Locomotor
            ('Dr. Pedro Castillo', 'Cirugía General'),
            ('Dra. Isabel Romero', 'Traumatología y Cirugía Ortopédica'),
            
            # Especialidades de Niños y Mujeres
            ('Dra. Lucía Mendoza', 'Pediatría'),
            ('Dr. Fernando Vega', 'Obstetricia y Ginecología'),
            
            # Ojos, Oídos y Vías Urinarias
            ('Dr. Roberto Silva', 'Oftalmología'),
            ('Dr. Antonio Navarro', 'Otorrinolaringología'),
            ('Dra. Carmen Rivas', 'Urología'),
            
            # Medicina Interna y Sistema Inmunológico
            ('Dr. Daniel Castro', 'Medicina Interna'),
            ('Dra. Mónica Ruíz', 'Inmunología'),
            
            # Pulmones y Riñones
            ('Dr. Jorge Ramos', 'Neumología'),
            ('Dra. Paola Herrera', 'Nefrología'),
            
            # Oncología
            ('Dr. Ernesto Soto', 'Oncología Médica'),
            ('Dra. Victoria Paz', 'Oncología Radioterápica'),
            
            # Otros
            ('Dr. Alejandro Vera', 'Anestesiología y Reanimación'),
            ('Dra. Natalia Cruz', 'Radiodiagnóstico'),
            ('Dr. Hugo Luna', 'Geriatría'),
            ('Dra. Sara Vidal', 'Alergología'),
            ('Dra. Clara Gil', 'Rehabilitación'),
            ('Dr. Emilio Ochoa', 'Reumatología'),
            ('Dra. Sonia Pérez', 'Medicina Intensiva'),
            ('Dr. Andrés Núñez', 'Medicina del Deporte'),
        ]
        
        cursor.executemany("INSERT INTO doctors (full_name, specialty) VALUES (?, ?)", doctores)
        print("Tabla 'doctors' populada con éxito con datos ampliados.")
        
    except sqlite3.Error as e:
        print(f"Error al popular la tabla de doctores: {e}")

def init_db():
    conn = sqlite3.connect('clinic.db') 
    cursor = conn.cursor()

    # Tabla de Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL 
    )
    ''')

    # --- TABLA DE PACIENTES MODIFICADA ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        dni TEXT UNIQUE, 
        phone TEXT,
        email TEXT,
        age INTEGER,
        height REAL, 
        weight REAL, 
        blood_type TEXT 
    )
    ''')

    # Tabla de Doctores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        specialty TEXT NOT NULL
    )
    ''')

    # Tabla de Historial Clínico
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clinical_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        doctor TEXT NOT NULL, 
        consultation_reason TEXT,
        diagnosis TEXT, 
        is_emergency INTEGER DEFAULT 0,
        blood_type TEXT,
        oncological_history TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )
    ''')

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       ('admin', 'admin123', 'admin'))
    except sqlite3.IntegrityError:
        pass 
    
    _populate_doctors_table(cursor)

    conn.commit()
    conn.close()

# --- Funciones de Usuarios y Pacientes ---

def check_login(username, password):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def create_user(username, password, role):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- FUNCIÓN MODIFICADA ---
def register_patient(full_name, dni=None, phone=None, email=None, age=None, height=None, weight=None, blood_type=None):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    new_patient_id = None
    
    dni_to_db = dni if (dni and dni != 'N/A') else None
    phone_to_db = phone if (phone and phone != 'N/A') else None
    email_to_db = email if (email and email != 'N/A') else None

    try:
        cursor.execute("""
            INSERT INTO patients (full_name, dni, phone, email, age, height, weight, blood_type) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, dni_to_db, phone_to_db, email_to_db, age, height, weight, blood_type))
        conn.commit()
        new_patient_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Error: Paciente con DNI {dni} ya existe.")
    finally:
        conn.close()
        return new_patient_id

def search_patient_by_name(name_query):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, dni FROM patients WHERE full_name LIKE ?", ('%' + name_query + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

# --- FUNCIÓN MODIFICADA ---
def get_patient_by_id(patient_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, dni, phone, email, age, height, weight, blood_type FROM patients WHERE id = ?", (patient_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# --- FUNCIÓN MODIFICADA (Renombrada de update_patient) ---
def update_patient_details(patient_id, full_name, dni, phone, email, age, height, weight, blood_type):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    dni_to_db = dni if (dni and dni.strip() != '') else None
    try:
        cursor.execute("""
            UPDATE patients 
            SET full_name = ?, dni = ?, phone = ?, email = ?, age = ?, height = ?, weight = ?, blood_type = ?
            WHERE id = ?
        """, (full_name, dni_to_db, phone, email, age, height, weight, blood_type, patient_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error: El DNI '{dni_to_db}' ya existe en otro paciente.")
        return False
    finally:
        conn.close()

def get_patient_history(patient_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clinical_history WHERE patient_id = ? ORDER BY appointment_date DESC", (patient_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# --- Funciones de Doctores ---
def get_all_doctors():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, specialty FROM doctors ORDER BY specialty, full_name")
    results = cursor.fetchall()
    conn.close()
    return results

def add_doctor(full_name, specialty):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO doctors (full_name, specialty) VALUES (?, ?)", (full_name, specialty))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al añadir doctor: {e}")
        return False
    finally:
        conn.close()

# --- Funciones de Citas / Historial ---

def add_emergency_record(patient_id, doctor, reason, diagnosis, blood_type, oncology):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    
    doc_to_db = doctor if (doctor and doctor != 'N/A') else "Doctor no asignado"
    reason_to_db = reason if (reason and reason != 'N/A') else "Motivo no especificado"
    diag_to_db = diagnosis if (diagnosis and diagnosis != 'N/A') else "Diagnóstico pendiente"

    cursor.execute("""
        INSERT INTO clinical_history 
        (patient_id, appointment_date, doctor, consultation_reason, diagnosis, is_emergency, blood_type, oncological_history)
        VALUES (?, strftime('%Y-%m-%d %H:%M', 'now'), ?, ?, ?, 1, ?, ?)
    """, (patient_id, doc_to_db, reason_to_db, diag_to_db, blood_type, oncology))
    conn.commit()
    conn.close()

def get_all_appointments_with_details():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ch.id, 
            p.full_name, 
            ch.appointment_date, 
            ch.doctor, 
            ch.consultation_reason,
            ch.diagnosis
        FROM 
            clinical_history ch
        LEFT JOIN 
            patients p ON ch.patient_id = p.id
        ORDER BY 
            ch.appointment_date DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def get_recent_appointments(limit=5):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ch.id, 
            p.full_name, 
            ch.appointment_date, 
            ch.doctor, 
            ch.consultation_reason,
            ch.diagnosis
        FROM 
            clinical_history ch
        LEFT JOIN 
            patients p ON ch.patient_id = p.id
        ORDER BY 
            ch.appointment_date DESC
        LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
    conn.close()
    return results


def get_appointment_by_id(appointment_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, appointment_date, doctor, consultation_reason, diagnosis FROM clinical_history WHERE id = ?", (appointment_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_appointment(appointment_id, new_date, new_doctor, new_reason, new_diagnosis):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE clinical_history
            SET appointment_date = ?, doctor = ?, consultation_reason = ?, diagnosis = ?
            WHERE id = ?
        """, (new_date, new_doctor, new_reason, new_diagnosis, appointment_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar cita: {e}")
        return False
    finally:
        conn.close()

def delete_appointment(appointment_id):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clinical_history WHERE id = ?", (appointment_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar cita: {e}")
        return False
    finally:
        conn.close()