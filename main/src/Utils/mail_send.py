import resend
from dotenv import load_dotenv
import os

load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

def enviar_correo_recuperacion(email, token):
    try:
        response = resend.Emails.send({
            "from": "Soporte Turismo <onboarding@resend.dev>",
            "to": email,
            "subject": "Recuperar Contraseña - PJD",
            "html": f"""
                <h3>Solicitud de recuperación de contraseña</h3>
                <p>Haz clic en el enlace para establecer una nueva clave (expira en 20 min):</p>
                <a href='{BASE_URL}/reset-password/{token}'>Establecer nueva contraseña</a>
                <p>Si no solicitaste este cambio, ignora este mensaje.</p>
            """
        })
        return True
    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False