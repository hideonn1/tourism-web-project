from src.Logica_de_Negocio.models.Destino import Destino

class Destino_Repository:
    
    def __init__(self, conectar_db):
        self._conectar_db = conectar_db

    def create(self, destino):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                    INSERT INTO destino (nombre, ciudad, pais, descripcion, actividades_disponibles, costo) 
                    VALUES (%s, %s, %s, %s, %s, 0);
                """)
            datos = (destino.nombre,
                     destino.ciudad,
                     destino.pais,
                     destino.descripcion,
                     destino.actividades_disponibles
                    )
            cursor.execute(query, datos)
            conexion.commit() 

            return destino
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()        
        
    
    def read_by_id(self, id_destino):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT * FROM destino WHERE id_destino = %s"
            datos = (id_destino,)
            cursor.execute(query,datos)
            resultado = cursor.fetchone()

            if resultado:
                destino_objeto = Destino(
                    id_destino = resultado['id_destino'],
                    nombre = resultado['nombre'],
                    ciudad = resultado['ciudad'],
                    pais = resultado['pais'],
                    descripcion = resultado['descripcion'],
                    actividades_disponibles = resultado['actividades_disponibles']
                )
                return destino_objeto 
            else:
                return None 

        finally:
            cursor.close()
            conexion.close() 

    def get_all(self):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT * FROM destino"
            cursor.execute(query)
            resultado = cursor.fetchall()
            
            destinos = []
            for res in resultado:
                destinos.append(Destino(
                    id_destino = res['id_destino'],
                    nombre = res['nombre'],
                    ciudad = res['ciudad'],
                    pais = res['pais'],
                    descripcion = res['descripcion'],
                    actividades_disponibles = res['actividades_disponibles']
                ))
            return destinos
        finally:
            cursor.close()
            conexion.close()

    def read_by_name(self, nombre):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT * FROM destino WHERE nombre = %s"
            datos = (nombre,)

            cursor.execute(query,datos)
            resultado = cursor.fetchone()

            if resultado:
                destino_objeto = Destino(
                    id_destino = resultado['id_destino'],
                    nombre = resultado['nombre'],
                    ciudad = resultado['ciudad'],
                    pais = resultado['pais'],
                    descripcion = resultado['descripcion'],
                    actividades_disponibles = resultado['actividades_disponibles']
                )
                return destino_objeto 
            else:
                return None 

        finally:
            cursor.close()
            conexion.close() 


    def update(self, destino):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                UPDATE destino SET 
                    nombre = %s,
                    ciudad = %s,
                    pais = %s,
                    descripcion = %s,
                    actividades_disponibles = %s
                WHERE id_destino = %s;
                """)
            datos = (destino.nombre,
                    destino.ciudad,
                    destino.pais,
                    destino.descripcion,
                    destino.actividades_disponibles,
                    destino.id_destino
                    )
            cursor.execute(query, datos)
            conexion.commit() 
            return destino
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()


    def delete(self, id_destino):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("DELETE FROM destino WHERE id_destino = %s;")
            datos = (id_destino,)
            cursor.execute(query, datos)
            conexion.commit() 
            return True 
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()


    def get_all_destinos(self, paquete_id):
        conexion = self._conectar_db()
        cursor = conexion.cursor(dictionary=True)
        try:
            query= """
                    SELECT
                        d.id_destino, d.nombre, d.ciudad, d.pais, d.descripcion,
                        d.actividades_disponibles,
                        dhp.orden_visita
                    FROM 
                        destino AS d
                    JOIN 
                        destino_has_paquete_turistico AS dhp 
                        ON d.id_destino = dhp.destino_id_destino
                    WHERE 
                        dhp.paquete_turistico_id_paquete_turistico = %s;"""
            datos = (paquete_id,)

            cursor.execute(query,datos)
            lista_destinos = cursor.fetchall()
            return lista_destinos
            
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conexion.close()

    def get_destinos_pais(self,pais):


        conexion = self._conectar_db()


        cursor = conexion.cursor(dictionary=True)


        try:


            query= """


                    SELECT


                        d.id_destino, d.nombre, d.ciudad, d.pais, d.descripcion,


                        d.actividades_disponibles


                    FROM 


                        destino AS d


                    WHERE 


                        d.pais = %s;"""


            datos = (pais,)





            cursor.execute(query,datos)


            lista_destinos = cursor.fetchall()


            return lista_destinos

        except Exception as e:


            print(e)


        finally:


            cursor.close()


            conexion.close()