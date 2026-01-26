from src.Logica_de_Negocio.models.Reserva import Reserva

class Reservas_Repository:
    
    def __init__(self, conectar_db):
        self._conectar_db = conectar_db

    def create(self, reserva, id_usuario, id_paquete):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query_1 = ("""
                    INSERT INTO reserva (estado, id_usuario, cupos) 
                    VALUES (%s, %s, %s);
                """)
            datos_1 = (reserva.estado,
                    id_usuario,
                    reserva.cupos
                    )

            cursor.execute(query_1, datos_1)
            conexion.commit() 

            reserva_id = cursor.lastrowid
            reserva.id_reserva = reserva_id

            query_2 = ("""INSERT INTO reserva_has_paquete_turistico 
                    (reserva_id_reserva, paquete_turistico_id_paquete_turistico) 
                    VALUES (%s, %s);""")
            datos_2 = (reserva_id, id_paquete,)

            cursor.execute(query_2,datos_2)

            query_3 = ("""UPDATE paquete_turistico
                    SET Cupos = Cupos - %s
                    WHERE id_paquete_turistico = %s;""")
            datos_3 = (reserva.cupos, id_paquete,)

            cursor.execute(query_3,datos_3)
            
            conexion.commit()
            return reserva
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()        
        
    
    def read_by_id(self, id_reserva):
        conexion = self._conectar_db() 
        cursor = conexion.cursor(dictionary=True)

        try:
            query = ("""SELECT
                        r.id_reserva,
                        r.id_usuario,
                        r.cupos,
                        r.estado,
                        rhp.paquete_turistico_id_paquete_turistico AS id_paquete_asociado
                    FROM
                        reserva AS r
                    JOIN
                        reserva_has_paquete_turistico AS rhp 
                        ON r.id_reserva = rhp.reserva_id_reserva 
                        WHERE r.id_reserva = %s;""")
            datos = (id_reserva,)

            cursor.execute(query,datos)
            resultado = cursor.fetchone()

            if resultado:
                reserva_objeto = Reserva(
                    id_reserva = resultado['id_reserva'],
                    id_usuario = resultado['id_usuario'],
                    cupos = resultado['cupos'],
                    estado = resultado['estado'],
                    id_paquete_turistico=resultado['id_paquete_asociado'],
                )
                return reserva_objeto
            else:
                return None 

        finally:
            cursor.close()
            conexion.close() 

    def update(self, reserva):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("""
                UPDATE reserva SET 
                    estado = %s, 
                    monto_total = %s
                WHERE id_reserva = %s;
                """)
            datos = (reserva.estado, 
                    reserva.monto_total,
                    reserva.id_reserva
                    )
            cursor.execute(query, datos)
            conexion.commit() 
            return reserva
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def delete(self, id_reserva):
        conexion = self._conectar_db()
        cursor = conexion.cursor()
        
        try:
            query = ("DELETE FROM reserva WHERE id_reserva = %s;")
            datos = (id_reserva,)
            cursor.execute(query, datos)
            conexion.commit() 
            return cursor.rowcount > 0
            
        except Exception as e:
            conexion.rollback()
            raise e
            
        finally:
            cursor.close()
            conexion.close()

    def read_by_usuario(self, id_usuario):
        conexion = self._conectar_db()
        cursor = conexion.cursor(dictionary=True)
        try:
            query = ("""SELECT
                        r.id_reserva,
                        r.id_usuario,
                        r.cupos,
                        r.estado,
                        pt.costo_paquete, 
                        rhp.paquete_turistico_id_paquete_turistico AS id_paquete_asociado
                    FROM
                        reserva AS r
                    JOIN
                        reserva_has_paquete_turistico AS rhp 
                        ON r.id_reserva = rhp.reserva_id_reserva 
                    JOIN
                        paquete_turistico AS pt 
                        ON rhp.paquete_turistico_id_paquete_turistico = pt.id_paquete_turistico 
                    WHERE
                        r.id_usuario = %s;""")
            cursor.execute(query, (id_usuario,))
            resultados = cursor.fetchall()
            reservas = [
                Reserva(
                    id_reserva=r['id_reserva'],
                    id_usuario=r['id_usuario'],
                    cupos=r['cupos'],
                    estado=r['estado'],
                    id_paquete_turistico=r['id_paquete_asociado']
                )
                for r in resultados
            ]
            return reservas
        finally:
            cursor.close()
            conexion.close()

    def read_all(self):
        conexion = self._conectar_db()
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT * FROM reserva"
            cursor.execute(query)
            resultados = cursor.fetchall()
            return [
                Reserva(
                    id_reserva=r['id_reserva'],
                    id_usuario=r['id_usuario'],
                    cupos=r['cupos'],
                    estado=r['estado'],
                )
                for r in resultados
            ]  
        finally:
            cursor.close()
            conexion.close()