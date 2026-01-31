import json
import base64
import hashlib
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class EncryptedSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False

class EncryptedCookieSessionInterface(SessionInterface):
    """
    Sesion interface que encripta la cookie usando AES-GCM.
    La 'app.secret_key' se usa para derivar la llave de encriptacion (HKDF podria ser mejor, 
    pero SHA256 es suficiente para este proposito simple).
    """
    
    def _get_key(self, app):
        # Derivar una lllave de 32 bytes desde la secret_key usando SHA256
        if not app.secret_key:
            return None
        return hashlib.sha256(app.secret_key.encode('utf-8')).digest()

    def open_session(self, app, request):
        cookie_val = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        if not cookie_val:
            return EncryptedSession()

        key = self._get_key(app)
        if not key:
            return EncryptedSession()

        try:
            # Formato esperado: nonce_b64.ciphertext_b64.tag_b64 (tag es parte de ciphertext en AESGCM usually appended)
            # Vamos a usar un formato simple: base64(nonce + ciphertext + tag)
            
            # Flask cookies por defecto usan . para separar, nosotros usaremos todo junto b64 o separado
            # Para simplicidad: nonce (12 bytes) + data_encriptada
            
            decoded_val = base64.urlsafe_b64decode(cookie_val)
            nonce = decoded_val[:12]
            ciphertext = decoded_val[12:]
            
            aesgcm = AESGCM(key)
            # Decrypt lanza excepcion si falla autenticacion (tag incorrecto)
            plain_data = aesgcm.decrypt(nonce, ciphertext, None)
            
            data = json.loads(plain_data.decode('utf-8'))
            return EncryptedSession(data)
        except Exception as e:
            # Si falla desencriptar (cookie vieja o ataque), retornamos sesion vacia
            # print(f"Error decrypting session: {e}")
            return EncryptedSession()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        
        # Si la sesion esta vacia, borrar cookie
        if not session:
            if session.modified:
                response.delete_cookie(
                    app.config['SESSION_COOKIE_NAME'], domain=domain, path=path
                )
            return

        key = self._get_key(app)
        if not key:
            return

        # Serializar y Encriptar
        data_json = json.dumps(dict(session))
        data_bytes = data_json.encode('utf-8')
        
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, data_bytes, None)
        
        # Combinar nonce + ciphertext y codificar b64
        # ciphertext incluye el tag de autenticacion al final
        combined = nonce + ciphertext
        cookie_val = base64.urlsafe_b64encode(combined).decode('utf-8')

        response.set_cookie(
            app.config['SESSION_COOKIE_NAME'],
            cookie_val,
            expires=self.get_expiration_time(app, session),
            httponly=True,
            domain=domain,
            path=path,
            secure=False, # Set to True if using HTTPS
            samesite='Lax'
        )
