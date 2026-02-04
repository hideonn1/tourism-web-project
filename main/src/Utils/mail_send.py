import resend
from dotenv import load_dotenv
import os
import logging

load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

def enviar_correo_recuperacion(email, token):
    try:
        logging.debug(f"DEBUG: mail_send.py - Intentando enviar a {email} con TOKEN: {token[:5]}...")
        response = resend.Emails.send({
            "from": "Soporte Explora360 <onboarding@resend.dev>",
            "to": email,
            "subject": "Recuperar contraseña de cuenta - Explora360",
            "html": f"""
                <h3>Solicitud de recuperación de contraseña</h3>
                <p>Haz click en el enlace para establecer una nueva clave (expira en 20 min):</p>
                <a href='{BASE_URL}/reset-password/{token}'>Establecer nueva contraseña</a>
                <p>Si no solicitaste este cambio, ignora este mensaje.</p>
            """
        })
        logging.debug(f"DEBUG: Respuesta Resend: {response}")
        return True
    except Exception as e:
        logging.error(f"Error al enviar email: {e}")
        return False