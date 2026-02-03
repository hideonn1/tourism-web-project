from .models.Usuario import Usuario
from datetime import date
import re

import bcrypt

class Usuario_Service:
    
    def __init__(self, usuario_repository):
        self._repo = usuario_repository 

    def obtener_usuario_por_id(self, id_usuario):
        return self._repo.get_by_id(id_usuario)

    def obtener_usuario_por_email(self, email):
        usuario_objeto = self._repo.get_by_email(email)
        return usuario_objeto
    
    def verificar_contrasena(self, email, contraseña_ingresada):
        usuario_objeto = self._repo.get_by_email(email)
        if usuario_objeto is None:
            raise ValueError(f"El usuario con email {email} no existe.")
        if bcrypt.checkpw(contraseña_ingresada.encode('utf-8'), usuario_objeto.contraseña_hash.encode('utf-8')):
            return True
        return False
    
    def nuevo_usuario(self, registro):
        usuario_objeto = Usuario(
            id_usuario=None,
            rut=registro['rut'],
            nombres=registro['nombre'],
            apellido_paterno=registro['apellido_paterno'],
            apellido_materno=registro['apellido_materno'],
            email=registro['email'],
            contraseña_hash=registro['contraseña'],
            telefono=registro['telefono'],
            fecha_nacimiento=registro['fecha_nacimiento'],
            fecha_registro=registro['fecha_registro'],
            rol=registro['rol']
        )
        self._repo.create(usuario_objeto)
        return True

    def registrar_usuario(self, data):
        # Unique validations
        if self._repo.get_by_email(data['email']):
            raise ValueError("El correo electrónico ya está registrado.")
        
        if self._repo.get_by_rut(data['rut']):
            raise ValueError("El RUT ya está registrado.")
            
        if self._repo.get_telefono(data['telefono']):
             raise ValueError("El número de teléfono ya está registrado.")

        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data['contrasena'].encode('utf-8'), salt).decode('utf-8')
        
        # Prepare full object for Repo (adapting simple form to DB schema)
        usuario_objeto = Usuario(
            id_usuario=None,
            rut=data['rut'],
            nombres=data['nombres'],
            apellido_paterno=data['apellido_paterno'],
            apellido_materno=data['apellido_materno'],
            email=data['email'],
            contraseña_hash=hashed,
            telefono=data['telefono'],
            fecha_nacimiento=date(2000, 1, 1), # Default filler
            fecha_registro=date.today(),
            rol=data['rol']
        )
        self._repo.create(usuario_objeto)
        return True

    def eliminar_usuario_admin(self, email):
        self._repo.delete(email)

    def eliminar_usuario_basico(self, email):
        self._repo.delete(email)
    
    def modificar_usuario_admin(self, email):
        self._repo.update(email)

    def modificar_usuario_basico(self, email):
        self._repo.update(email)

    def validador_rut(self, rut):
        rut = rut.strip().lower()
        if rut.count('-') != 1:
            raise ValueError("El RUT debe contener un solo guion ('-').")

        parte_num, dv = rut.split('-')

        if len(rut) < 9 or len(rut) > 10:
            raise ValueError("El RUT debe tener entre 9 y 10 caracteres en total.")

        if not parte_num.isdigit():
            raise ValueError("Los caracteres antes del guion deben ser solo números.")

        if len(parte_num) not in [7, 8]:
            raise ValueError("La parte numérica del RUT debe tener 7 u 8 dígitos.")

        if dv not in ['0','1','2','3','4','5','6','7','8','9','k']:
            raise ValueError("El dígito verificador debe ser un número o la letra 'k'.")

        return rut.upper(), True

    def mayor_a_18(self, fecha_nacimiento):
        hoy = date.today()

        fecha_cumple_18 = fecha_nacimiento.replace(year=fecha_nacimiento.year + 18)

        if hoy >= fecha_cumple_18:
            return True
        else:
            return False
        
    def verificar_numero(self, numero):
        return self._repo.get_telefono(numero)

    def obtener_usuario_por_rut(self, rut):
        return self._repo.get_by_rut(rut)

    def verificador_contraseña(self, contraseña_nueva):
        return self._repo.get_contraseña(contraseña_nueva)

    def actual_usuario_contacto(self, id_usuario, nuevo_email, nuevo_telefono):
        # Fetch current user
        usuario = self._repo.get_by_id(id_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # Validate Email (simple regex)
        if nuevo_email and not re.match(r"[^@]+@[^@]+\.[^@]+", nuevo_email):
            raise ValueError("Formato de email inválido")
        
        # Log and Update Email
        if nuevo_email and nuevo_email != usuario.email:
            # log_change(id_usuario, 'email', usuario.email, nuevo_email)
            usuario.email = nuevo_email
        
        if nuevo_telefono:
            # Format: +56 9 1234 5678
            if not re.match(r"^\+56 9 [0-9]{4} [0-9]{4}$", nuevo_telefono):
                raise ValueError("Formato de teléfono inválido. Debe ser: +56 9 1234 5678")
            
            if nuevo_telefono != usuario.telefono:
                # log_change(id_usuario, 'telefono', usuario.telefono, nuevo_telefono)
                usuario.telefono = nuevo_telefono
            
        # Persist changes
        self._repo.update(usuario)
        return True

    def restablecer_contrasena(self, rut, nueva_contrasena):
        # Hash de la nueva contraseña
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), salt).decode('utf-8')
        
        # Llamar al repositorio para actualizar
        return self._repo.actualizar_contrasena(rut, hashed)
