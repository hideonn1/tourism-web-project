import secrets
import hashlib
from datetime import datetime, timedelta

def generar_token_recuperacion():
    token_url = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token_url.encode()).hexdigest()
    expiracion = datetime.now() + timedelta(minutes=20)
    return token_url, token_hash, expiracion

def verificar_token_recuperacion(token_plano_usuario, hash_db, expiracion_db):
    if datetime.now() > expiracion_db:
        return False
    hash_intento = hashlib.sha256(token_plano_usuario.encode()).hexdigest()
    return hash_intento == hash_db