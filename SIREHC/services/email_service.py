import smtplib
from email.message import EmailMessage

def enviar_correo_cita(destinatario, fecha, doctor, consultorio):
    msg = EmailMessage()
    msg.set_content(f"Hola, tu cita ha sido programada.\n\nFecha: {fecha}\nDoctor: {doctor}\nConsultorio: {consultorio}")

    msg['Subject'] = 'Confirmación de Cita Médica'
    msg['From'] = 'tu-correo@gmail.com'
    msg['To'] = destinatario

    # Conexión al servidor de Gmail
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('tu-correo@gmail.com', 'TU-PASSWORD-DE-APP') 
        server.send_message(msg)
        server.quit()
        print("Correo enviado!")
    except Exception as e:
        print(f"Error al enviar correo: {e}")