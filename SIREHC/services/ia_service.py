# services/ia_service.py
from openai import OpenAI
import json

# -----------------------------------------------------------------
# Pega tu clave API real aquí
# -----------------------------------------------------------------
API_KEY = "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"
# -----------------------------------------------------------------


# Inicializamos el cliente de OpenAI
try:
    client = OpenAI(api_key=API_KEY)
except Exception as e:
    print(f"Error al inicializar cliente de OpenAI: {e}")
    client = None

def obtener_cita_ia(prompt_usuario):
    """
    Toma el texto de un usuario y lo convierte en datos de cita usando IA.
    """
    if not client:
        return '{"error": "Cliente de OpenAI no inicializado."}'

    # --- INICIO DE LA MEJORA (NUEVOS CAMPOS) ---
    system_prompt = """
    Eres un asistente de triaje médico. Tu trabajo es analizar la petición del usuario
    y devolverla SOLAMENTE en formato JSON.
    
    Los campos que debes rellenar son: 
    1. 'paciente': Nombre del paciente.
    2. 'dni': DNI del paciente.
    3. 'phone': Teléfono del paciente.
    4. 'doctor': El doctor específico si se menciona (ej. "Dr. Pérez").
    5. 'fecha': La fecha y/o hora de la cita.
    6. 'motivo': El síntoma o razón principal (ej. "dolor de cabeza", "chequeo general").
    7. 'posible_enfermedad': Basado en el 'motivo', indica una posible condición (ej: "Migraña", "Gastroenteritis").
    8. 'especialista_recomendado': El tipo de especialista médico recomendado basado en el 'motivo' (ej: 'Gastroenterólogo', 'Cardiología', 'Neurólogo').
    9. 'age': Edad del paciente (si se menciona).
    10. 'height': Altura del paciente en metros (ej. 1.70) (si se menciona).
    11. 'weight': Peso del paciente en kg (ej. 75) (si se menciona).
    12. 'blood_type': Tipo de sangre (ej. "O+") (si se menciona).

    REGLAS:
    - Si el usuario NO menciona un doctor, usa el 'motivo' para deducir el 'especialista_recomendado'.
    - Rellena todos los campos. Si un dato no se encuentra, usa 'N/A'.
    - Tu respuesta debe ser SIEMPRE un JSON válido, sin texto de introducción.

    EJEMPLOS:
    
    Usuario: "Soy Jair Machaca, DNI 778899, tengo 30 años, mido 1.70, peso 75kg y mi sangre es O+"
    Tu respuesta: {"paciente": "Jair Machaca", "dni": "778899", "phone": "N/A", "doctor": "N/A", "fecha": "N/A", "motivo": "N/A", "posible_enfermedad": "N/A", "especialista_recomendado": "N/A", "age": 30, "height": 1.70, "weight": 75, "blood_type": "O+"}

    Usuario: "mi hijo tiene dolor de estomago persistente y fiebre, necesito una cita"
    Tu respuesta: {"paciente": "hijo", "dni": "N/A", "phone": "N/A", "doctor": "N/A", "fecha": "N/A", "motivo": "dolor de estomago persistente y fiebre", "posible_enfermedad": "Gastroenteritis", "especialista_recomendado": "Gastroenterólogo", "age": "N/A", "height": "N/A", "weight": "N/A", "blood_type": "N/A"}
    """
    # --- FIN DE LA MEJORA ---

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_usuario}
            ],
            response_format={"type": "json_object"}
        )
        
        respuesta_json = completion.choices[0].message.content
        return respuesta_json

    except Exception as e:
        print(f"Error en la llamada a la API de OpenAI: {e}")
        error_msg = str(e).replace('"', "'")
        return f'{{"error": "No se pudo contactar a la IA: {error_msg}"}}'