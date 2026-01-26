from src.Logica_de_Negocio.models.Usuario import Usuario
import mysql.connector

class Usuario_Repository:
    
    def __init__(self, conectar_db):
        self._conectar_db = conectar_db

    def create(self, usuario):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                    INSERT INTO usuario (rut, nombres, apellido_paterno, apellido_materno, email, contraseña, rol, telefono, fecha_nacimiento, fecha_registro) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """)
            datos = (usuario.rut,
                     usuario.nombres,
                     usuario.apellido_paterno,
                     usuario.apellido_materno,
                     usuario.email,
                     usuario.contraseña,
                     usuario.rol,
                     usuario.telefono,
                     usuario.fecha_nacimiento,
                     usuario.fecha_registro
                    )
            cursor.execute(query, datos)
            conexion.commit() 

            return usuario
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()        
               
    def get_by_id(self, id_usuario):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM usuario WHERE id_usuario = %s"
            datos = (id_usuario,)
            cursor.execute(query, datos)
            resultado = cursor.fetchone()

            if resultado:
                return Usuario(
                    id_usuario=resultado['id_usuario'],
                    rut=resultado['rut'],
                    nombres=resultado['nombres'],
                    apellido_paterno=resultado['apellido_paterno'],
                    apellido_materno=resultado['apellido_materno'],
                    email=resultado['email'],
                    contraseña_hash=resultado['contraseña'],
                    telefono=resultado['telefono'],
                    fecha_nacimiento=resultado['fecha_nacimiento'],
                    fecha_registro=resultado['fecha_registro'],
                    rol=resultado['rol']
                )
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def get_by_email(self, email):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM usuario WHERE email = %s"
            datos = (email,)
            cursor.execute(query, datos)
            resultado = cursor.fetchone()

            if resultado:
                return Usuario(
                    id_usuario=resultado['id_usuario'],
                    rut=resultado['rut'],
                    nombres=resultado['nombres'],
                    apellido_paterno=resultado['apellido_paterno'],
                    apellido_materno=resultado['apellido_materno'],
                    email=resultado['email'],
                    contraseña_hash=resultado['contraseña'],
                    telefono=resultado['telefono'],
                    fecha_nacimiento=resultado['fecha_nacimiento'],
                    fecha_registro=resultado['fecha_registro'],
                    rol=resultado['rol']
                )
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def get_by_rut(self, rut):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM usuario WHERE rut = %s"
            datos = (rut,)
            cursor.execute(query, datos)
            resultado = cursor.fetchone()

            if resultado:
                return Usuario(
                    id_usuario=resultado['id_usuario'],
                    rut=resultado['rut'],
                    nombres=resultado['nombres'],
                    apellido_paterno=resultado['apellido_paterno'],
                    apellido_materno=resultado['apellido_materno'],
                    email=resultado['email'],
                    contraseña_hash=resultado['contraseña'],
                    telefono=resultado['telefono'],
                    fecha_nacimiento=resultado['fecha_nacimiento'],
                    fecha_registro=resultado['fecha_registro'],
                    rol=resultado['rol']
                )
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def update(self, usuario):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                UPDATE usuario SET 
                    nombres = %s, 
                    apellido_paterno = %s, 
                    apellido_materno = %s, 
                    email = %s, 
                    telefono = %s, 
                    contraseña = %s 
                WHERE id_usuario = %s;
                """)
            datos = (usuario.nombres, 
                    usuario.apellido_paterno, 
                    usuario.apellido_materno, 
                    usuario.email, 
                    usuario.telefono, 
                    usuario.contraseña,
                    usuario.id_usuario
                    )
            cursor.execute(query, datos)
            conexion.commit() 
            return usuario 
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def delete(self, email):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("DELETE FROM usuario WHERE email = %s;")
            datos = (email,)
            cursor.execute(query, datos)
            conexion.commit() 
            return True 
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def get_contraseña(self, contraseña_actual):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM Usuario WHERE contraseña = %s"
            datos = (contraseña_actual,)

            cursor.execute(query,datos)
            resultado = cursor.fetchone()

            if resultado:
                return True 
            else:
                return False

        finally:
            pass 

    def get_telefono(self, telefono):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM Usuario WHERE telefono = %s"
            datos = (telefono,)

            cursor.execute(query,datos)
            resultado = cursor.fetchone()

            if resultado:
                return True 
            else:
                return False 

        finally:
            pass 
