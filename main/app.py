from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
from config import conectar_db
from src.Datos.usuario_repository import Usuario_Repository
from src.Logica_de_Negocio.usuarios_service import Usuario_Service
from src.Datos.destino_repository import Destino_Repository
from src.Logica_de_Negocio.destino_service import Destino_Service
from src.Datos.paquete_turistico_repository import Paquete_Repository
from src.Logica_de_Negocio.paquete_turistico_service import Paquete_Service
from src.Datos.reserva_repository import Reservas_Repository
from src.Logica_de_Negocio.reservas_service import Reservas_Service
from mysql.connector import Error
from src.Utils.img_conversor_tool import procesar_todas_las_imagenes
from src.Utils.security import generar_token_recuperacion, verificar_token_recuperacion
from src.Utils.mail_send import enviar_correo_recuperacion
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Fix para obtener la IP real detrás de Docker/Proxy (Importante para producción)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

if os.environ.get('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
else:
    app.config['SESSION_COOKIE_SECURE'] = False
    print("\n")
    print("Advertencia: SESSION_COOKIE_SECURE está deshabilitado. No uses esta aplicación en producción.")
    print("\n")

from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Configurar Session Interface Encriptada (AES-GCM)
from src.Utils.encrypted_session import EncryptedCookieSessionInterface
app.session_interface = EncryptedCookieSessionInterface()

# Configurar Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Repositorios y Servicios
usuario_repo = Usuario_Repository(conectar_db)
usuario_serv = Usuario_Service(usuario_repo)

destino_repo = Destino_Repository(conectar_db)
destino_serv = Destino_Service(destino_repo)

paquete_repo = Paquete_Repository(conectar_db)
paquete_serv = Paquete_Service(paquete_repo, destino_repo)

reserva_repo = Reservas_Repository(conectar_db)
reserva_serv = Reservas_Service(reserva_repo)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre-nosotros')
def about():
    return render_template('about.html')

@app.route('/contacto')
def contact():
    return render_template('contact.html')

@app.route('/politica-privacidad')
def privacy():
    return render_template('privacy.html')

# --- API ENDPOINTS ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or request.form
    email = data.get('email')
    password = data.get('password')
    
    try:
        if usuario_serv.verificar_contrasena(email, password):
            usuario = usuario_serv.obtener_usuario_por_email(email)
            session['user_id'] = usuario.id_usuario
            session['rol'] = usuario.rol
            return jsonify({
                'success': True, 
                'usuario': usuario.to_dict()
            })
        else:
             return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or request.form
    try:
        import re
        # Validaciones explicitas
        if not re.match(r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$", data.get('nombres', '')):
             raise ValueError("El nombre solo debe contener letras.")
        if not re.match(r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$", data.get('apellido_paterno', '')):
             raise ValueError("El apellido paterno solo debe contener letras.")
        # Materno is optional, but if present must be letters
        if data.get('apellido_materno') and not re.match(r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$", data.get('apellido_materno', '')):
             raise ValueError("El apellido materno solo debe contener letras.")
        
        # Validate Phone
        telefono = data.get('telefono', '')
        if not re.match(r"^\+56 9 [0-9]{4} [0-9]{4}$", telefono):
            raise ValueError("El formato del teléfono es incorrecto. Debe ser: +56 9 1234 5678")

        # Validate RUT (Simple regex check, full logic in service if needed)
        rut = data.get('rut', '')
        if not re.match(r"^[0-9]+-[0-9kK]$", rut):
             raise ValueError("El formato del RUT es incorrecto. Debe ser sin puntos y con guión (ej: 12345678-9)")

        # Validate Password Strength
        password = data.get('password', '')
        # Min 8 chars, at least 1 letter, 1 number, 1 special char
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[#$%&/!\"?¿'@]).{8,}$", password):
            raise ValueError("La contraseña debe tener al menos 8 caracteres, incluir letras, 1 número y 1 carácter especial.")

        # Create user dictionary for service
        user_data = {
            "nombres": data.get('nombres', '').title(),
            "apellido_paterno": data.get('apellido_paterno', '').title(),
            "apellido_materno": data.get('apellido_materno', '').title(), # Optional
            "rut": data.get('rut'),
            "email": data.get('email'),
            "telefono": data.get('telefono'),
            "contrasena": data.get('password'),
            "rol": "Cliente" # Default role
        }
        
        # Use service to register (assuming it handles hashing)
        usuario_serv.registrar_usuario(user_data)
        
        return jsonify({'success': True, 'message': 'Usuario registrado exitosamente'})
    except ValueError as ve:
        return jsonify({'success': False, 'message': str(ve)}), 400
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Error al registrar usuario'}), 500

@app.route('/api/me', methods=['GET', 'PUT'])
def my_account():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    
    user_id = session['user_id']
    
    if request.method == 'GET':
        usuario = usuario_serv.obtener_usuario_por_id(user_id)
        if usuario:
            return jsonify({
                'success': True,
                'usuario': usuario.to_dict()
            })
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    if request.method == 'PUT':
        data = request.json
        nuevo_email = data.get('email')
        nuevo_telefono = data.get('telefono')
        
        try:
            usuario_serv.actual_usuario_contacto(user_id, nuevo_email, nuevo_telefono)
            return jsonify({'success': True, 'message': 'Datos actualizados correctamente'})
        except ValueError as ve:
            return jsonify({'success': False, 'message': str(ve)}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/destinos', methods=['GET', 'POST'])
def destinos():
    if request.method == 'GET':
        try:
            destinos = destino_serv.obtener_todos()
            return jsonify([d.to_dict() for d in destinos])
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    if request.method == 'POST':
        if session.get('rol') != 'Administrador':
            return jsonify({'success': False, 'message': 'No autorizado'}), 403
            
        data = request.json
        try:
            # Adapt data for constructor
            # Destino model expects: nombre, ciudad, pais, descripcion, actividades_disponibles, costo
            registro = {
                "nombre": data.get('nombre'),
                "ciudad": data.get('ciudad'),
                "pais": data.get('pais'),
                "descripcion": data.get('descripcion'),
                "actividades_disponibles": data.get('actividades_disponibles')
            }
            destino_serv.nuevo_destino(registro)
            return jsonify({'success': True, 'message': 'Destino creado'})
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/destinos/<int:id>', methods=['DELETE'])
def eliminar_destino(id):
    if session.get('rol') != 'Administrador':
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    try:
        destino_serv.eliminar_destino(id)
        return jsonify({'success': True, 'message': 'Destino eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/paquetes', methods=['GET', 'POST'])
def paquetes():
    if request.method == 'GET':
        try:
            paquetes = paquete_serv.obtener_todos()
            return jsonify([p.to_dict() for p in paquetes])
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    if request.method == 'POST':
         if session.get('rol') != 'Administrador':
            return jsonify({'success': False, 'message': 'No autorizado'}), 403
         data = request.json
         try:
             # Paquete expects object, service.agregar_paquete(paquete)
             # We need to construct PaqueteTuristico object
             from src.Logica_de_Negocio.models.PaqueteTuristico import PaqueteTuristico
             from datetime import datetime

             fecha_salida_str = data.get('fecha_salida')
             fecha_llegada_str = data.get('fecha_llegada')

             fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
             fecha_llegada = datetime.strptime(fecha_llegada_str, '%Y-%m-%d').date()

             # Validaciones de negocio
             val_salida = paquete_serv.confirmar_fecha_salida(fecha_salida)
             if val_salida != True:
                 return jsonify({'success': False, 'message': val_salida}), 400
            
             val_llegada = paquete_serv.confirmar_fecha_llegada(fecha_llegada, fecha_salida)
             if val_llegada != True:
                 return jsonify({'success': False, 'message': val_llegada}), 400

             nuevo_paquete = PaqueteTuristico(
                 fecha_salida=fecha_salida,
                 fecha_llegada=fecha_llegada,
                 costo_destino=int(data.get('costo_destino')),
                 cupos=int(data.get('cupos')),
                 modalidad="Nacional" # Default, logic updates it
             )
             paquete_creado = paquete_serv.agregar_paquete(nuevo_paquete)
             
             # Link Destinos
             destinos_ids = data.get('destinos', [])
             for d_id in destinos_ids:
                 destino_obj = destino_serv.obtener_destino_por_id(d_id)
                 if destino_obj:
                     paquete_serv.agregar_destino_a_paquete(paquete_creado, destino_obj)

             return jsonify({'success': True, 'message': 'Paquete creado con destinos'})
         except ValueError as ve:
             return jsonify({'success': False, 'message': f'Error de formato de fecha o valor: {str(ve)}'}), 400
         except Exception as e:
             return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/paquetes/<int:id>', methods=['DELETE'])
def eliminar_paquete(id):
    if session.get('rol') != 'Administrador':
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    try:
        paquete_serv.quitar_paquete(id)
        return jsonify({'success': True, 'message': 'Paquete eliminado'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/reservas', methods=['POST'])
def crear_reserva():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    
    data = request.json
    try:
        # Check cupos availability via service (logic to be verified or added)
        # Assuming package exists and user is logged in
        id_paquete = data.get('id_paquete')
        cupos = int(data.get('cupos'))
        
        # Verify quotas
        if not paquete_serv.verificar_cupos(id_paquete, cupos):
             return jsonify({'success': False, 'message': 'No hay suficientes cupos'}), 400

        datos_reserva = {
            "estado": "Confirmada", # Initial state
            "cupos": cupos
        }
        reserva_serv.crear_reserva(datos_reserva, session['user_id'], id_paquete)
        
        return jsonify({'success': True, 'message': 'Reserva creada'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/mis-reservas', methods=['GET'])
def mis_reservas():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    try:
        reservas = reserva_serv.obtener_reservas_por_usuario(session['user_id'])
        return jsonify([r.to_dict() for r in reservas])
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500


FOLDER_ORIGINALS = os.path.join('static', 'img', 'original-photo-web')
FOLDER_OPTIMIZED = os.path.join('static', 'img')

os.makedirs(FOLDER_ORIGINALS, exist_ok=True)
os.makedirs(FOLDER_OPTIMIZED, exist_ok=True)

@app.route('/api/convertir-imagenes', methods=['POST'])
def convertir_imagenes():
    if session.get('rol') != 'Administrador':
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    try:
        procesar_todas_las_imagenes()
        return jsonify({'success': True, 'message': 'Imagenes convertidas exitosamente'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/forgot-password', methods=['GET', 'POST'])
@limiter.limit("3 per hour")  # Límite general
@limiter.limit("5 per minute") # Prevenir spam rápido (ajustado para ser menos agresivo)
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        db = conectar_db()
        cursor = db.cursor(dictionary=True)

        try:
            # 1. Buscamos al usuario por email para obtener su RUT
            cursor.execute("SELECT rut FROM usuario WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            # TIP de Seguridad: Siempre mostrar el mismo mensaje
            mensaje_estandar = "Si el correo está registrado, recibirás un enlace pronto."

            if usuario:
                rut_usuario = usuario['rut']
                
                # 2. Generamos el token usando security.py
                token_plano, t_hash, expiracion = generar_token_recuperacion()

                # 3. Guardamos en la tabla password_resets
                sql = """INSERT INTO password_resets (user_rut, token_hash, expires_at) 
                         VALUES (%s, %s, %s)"""
                cursor.execute(sql, (rut_usuario, t_hash, expiracion))
                db.commit()

                # 4. Enviamos el correo
                print(f"DEBUG: Enviando correo a {email}...")
                exito = enviar_correo_recuperacion(email, token_plano)
                print(f"DEBUG: Resultado envio correo: {exito}")
            else:
                print(f"DEBUG: Usuario con email {email} NO encontrado en la BD.")
            
            flash(mensaje_estandar, "info")
            
        except Exception as e:
            print(f"Error en forgot_password: {e}")
            flash("Ocurrió un error al procesar la solicitud.", "danger")
        finally:
            cursor.close()
            db.close()
            
        return redirect(url_for('index')) # Redirect to index (login modal)

    return render_template('forgot_password.html')



@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    import hashlib
    token_hash_busqueda = hashlib.sha256(token.encode()).hexdigest()

    db = conectar_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Buscamos el registro y verificamos que no haya expirado
        sql = "SELECT * FROM password_resets WHERE token_hash = %s AND expires_at > NOW()"
        cursor.execute(sql, (token_hash_busqueda,))
        reseteo = cursor.fetchone()

        if not reseteo:
            flash("El enlace es inválido o ha expirado.", "danger")
            return redirect(url_for('forgot_password'))

        if request.method == 'POST':
            nueva_clave = request.form.get('password')
            confirm_clave = request.form.get('confirm_password')

            if nueva_clave != confirm_clave:
                flash("Las contraseñas no coinciden.", "danger")
                return render_template('reset_password.html', token=token)

            # Usar servicio para actualizar contraseña de forma segura (hasheada)
            usuario_serv.restablecer_contrasena(reseteo['user_rut'], nueva_clave)
            
            # Borrar el token usado
            cursor.execute("DELETE FROM password_resets WHERE user_rut = %s", 
                           (reseteo['user_rut'],))
            db.commit()
            
            flash("Contraseña actualizada con éxito. Inicia sesión.", "success")
            return redirect(url_for('index')) # Back to home/login
            
    except Exception as e:
        print(f"Error en reset_password: {e}")
        flash("Ocurrió un error al restablecer la contraseña.", "danger")
        return redirect(url_for('forgot_password'))
    finally:
        cursor.close()
        db.close()

    return render_template('reset_password.html', token=token)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
