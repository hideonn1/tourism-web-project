from src.Logica_de_Negocio.models.PaqueteTuristico import PaqueteTuristico

class Paquete_Repository:
    
    def __init__(self, conectar_db):
        self._conectar_db = conectar_db

    def create(self, paquete):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                    INSERT INTO paquete_turistico (costo_paquete, fecha_inicio, fecha_final, modalidad, cupos) 
                    VALUES (%s,%s,%s,%s,%s);
                """)
            datos = (paquete.costo_destino, paquete.fecha_salida, paquete.fecha_llegada, paquete.modalidad, paquete.cupos
                    )
            cursor.execute(query, datos)
            conexion.commit() 

            paquete_id = cursor.lastrowid
            paquete.id_paquete = paquete_id

            return paquete
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()        
        
    def read_by_id(self, id_paquete):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM paquete_turistico WHERE id_paquete_turistico = %s"
            datos = (id_paquete,)

            cursor.execute(query,datos)
            resultado = cursor.fetchone()

            if resultado:
                paquete_objeto = PaqueteTuristico(
                    id_paquete = resultado['id_paquete_turistico'],
                    fecha_llegada = resultado['fecha_final'],
                    fecha_salida = resultado['fecha_inicio'],
                    costo_destino = resultado['costo_paquete'],
                    modalidad = resultado['modalidad'],
                    cupos = resultado['cupos']
                )
                return paquete_objeto
            else:
                return None 

        finally:
            cursor.close()
            conexion.close() 

    def get_all(self):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT * FROM paquete_turistico"
            cursor.execute(query)
            resultado = cursor.fetchall()
            
            paquetes = []
            for res in resultado:
                paquetes.append(PaqueteTuristico(
                    id_paquete = res['id_paquete_turistico'],
                    fecha_llegada = res['fecha_final'],
                    fecha_salida = res['fecha_inicio'],
                    costo_destino = res['costo_paquete'],
                    modalidad = res['modalidad'],
                    cupos = res['cupos']
                ))
            return paquetes
        finally:
            cursor.close()
            conexion.close()

    def update(self, paquete_turistico):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        try:
            query = ("""
                UPDATE paquete_turistico SET 
                    fecha_final = %s,
                    fecha_inicio = %s,
                    costo_paquete = %s,
                    modalidad = %s
                WHERE id_paquete_turistico = %s;
                """)
            datos = (paquete_turistico.fecha_llegada,
                    paquete_turistico.fecha_salida,
                    paquete_turistico.costo_destino,
                    paquete_turistico.modalidad,
                    paquete_turistico.id_paquete
                    )
            cursor.execute(query, datos)
            conexion.commit() 
            return paquete_turistico
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def delete(self, id_paquete_turistico):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("DELETE FROM paquete_turistico WHERE id_paquete_turistico = %s;")
            datos = (id_paquete_turistico,)
            cursor.execute(query, datos)
            conexion.commit() 
            return cursor.rowcount > 0
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def destino_x_paquete(self, paquete, destino):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                    INSERT INTO destino_has_paquete_turistico (destino_id_destino, paquete_turistico_id_paquete_turistico, fecha_llegada, fecha_salida, orden_visita) 
                    VALUES (%s, %s, %s, %s, %s);
                """)
            datos = (destino.id_destino,
                    paquete.id_paquete,
                    destino.fecha_llegada,
                    destino.fecha_salida,
                    destino.orden_visita
                    )
            cursor.execute(query, datos)
            conexion.commit() 
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()     

    def duplicidad_destino(self, destino_id, paquete_id):

        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = """
                SELECT 1 FROM destino_has_paquete_turistico 
                WHERE destino_id_destino = %s 
                AND paquete_turistico_id_paquete_turistico = %s 
                LIMIT 1;
            """
            datos = (destino_id, paquete_id)
            
            cursor.execute(query, datos)
            
            resultado = cursor.fetchone()
            
            return resultado is not None 

        except Exception as e:
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def obtener_destino(self, paquete_id,orden_visita):
        conexion = self._conectar_db()
        cursor = conexion.cursor(dictionary=True)
        
        try:
            query = """
                SELECT * FROM destino_has_paquete_turistico 
                WHERE orden_visita = %s
                AND paquete_turistico_id_paquete_turistico = %s 
                LIMIT 1;
            """
            datos = (orden_visita, paquete_id)
            
            cursor.execute(query, datos)
            
            resultado = cursor.fetchone()
            
            return resultado

        except Exception as e:
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def eliminar_destino(self, id_paquete, orden_visita, dias):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query_1 = """
                DELETE FROM destino_has_paquete_turistico 
                WHERE paquete_turistico_id_paquete_turistico = %s
                AND orden_visita = %s;"""
            datos_1 = (id_paquete,orden_visita,)

            cursor.execute(query_1, datos_1)
            dias_int = int(dias)
            query_3 = """
                UPDATE destino_has_paquete_turistico
                SET 
                    fecha_llegada = DATE_SUB(fecha_llegada, INTERVAL %s DAY),
                    fecha_salida = DATE_SUB(fecha_salida, INTERVAL %s DAY)
                WHERE 
                    paquete_turistico_id_paquete_turistico = %s
                    AND orden_visita > %s;
            """
            datos_3 = (dias_int, dias_int, id_paquete, orden_visita)
            
            cursor.execute(query_3, datos_3)

            query_2 = """
                UPDATE destino_has_paquete_turistico
                SET orden_visita = orden_visita - 1
                WHERE paquete_turistico_id_paquete_turistico = %s
                AND orden_visita > %s;"""
            
            datos_2 = (id_paquete, orden_visita,)

            cursor.execute(query_2, datos_2)
            conexion.commit()


        except Exception as e:
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def eliminar_paquete(self, id_paquete) :
        """
        Elimina un paquete turístico por su ID. 
        Las referencias en destino_has_paquete_turistico se eliminan automáticamente 
        gracias a la configuración ON DELETE CASCADE.
        """
        conexion = None
        cursor = None
        
        try:
            conexion = self._conectar_db()
            cursor = conexion.cursor()
            
            query = """
                DELETE FROM paquete_turistico 
                WHERE id_paquete_turistico = %s;
            """
            params = (id_paquete,)
            
            cursor.execute(query, params)
            
            conexion.commit() 
            
            return cursor.rowcount > 0 

        except Exception as e:
            if conexion:
                conexion.rollback()

            raise e
            
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def get_ultimo_orden_visita(self, id_paquete):
            conexion = None
            cursor = None
            
            try:
                conexion = self._conectar_db()
                cursor = conexion.cursor() 
                query = """
                    SELECT MAX(orden_visita) 
                    FROM destino_has_paquete_turistico
                    WHERE paquete_turistico_id_paquete_turistico = %s;
                """
                params = (id_paquete,)
                
                cursor.execute(query, params)
                
                resultado = cursor.fetchone() 
                
                ultimo_orden = resultado[0] if resultado and resultado[0] is not None else 0
                
                return ultimo_orden

            except Exception as e:
                raise e
                
            finally:
                if cursor:
                    cursor.close()
                if conexion:
                    conexion.close()

    def traer_paquetes(self, modalidad):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = "SELECT * FROM paquete_turistico WHERE modalidad = %s"
            datos = (modalidad,)

            cursor.execute(query,datos)

            lista_paquetes = cursor.fetchall()

            return lista_paquetes


        finally:
            cursor.close()
            conexion.close() 