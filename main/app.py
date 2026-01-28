from flask import Flask, render_template, request, jsonify, session
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

app = Flask(__name__)
app.secret_key =  'CLAVE_ELIMINADA_POR_SEGURIDAD'# Cambiar en produccion

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
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        if usuario_serv.verificar_contrasena(email, password):
            usuario = usuario_serv.obtener_usuario_por_email(email)
            session['user_id'] = usuario.id_usuario
            session['rol'] = usuario.rol
            return jsonify({
                'success': True, 
                'usuario': {
                    'id': usuario.id_usuario,
                    'nombre': usuario.nombres,
                    'apellido_paterno': usuario.apellido_paterno,
                    'email': usuario.email,
                    'telefono': usuario.telefono,
                    'rol': usuario.rol
                }
            })
        else:
             return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
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
             paquete_serv.agregar_paquete(nuevo_paquete)
             return jsonify({'success': True, 'message': 'Paquete creado'})
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

if __name__ == '__main__':
    app.run(debug=True)
