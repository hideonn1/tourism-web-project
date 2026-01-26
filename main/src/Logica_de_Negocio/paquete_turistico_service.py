from datetime import timedelta, date
class Paquete_Service:
    def __init__(self, paquete_repository, destino_repository):
        self._repo = paquete_repository
        self._repo_destino = destino_repository

    def obtener_multiplicador(self, fecha_salida):
        mes = fecha_salida.month  

        if mes in (7, 9):  
            return 1.2
        elif mes in (1, 2): 
            return 1.3
        elif mes in (12, 3): 
            return 1.1
        elif mes in (6, 4, 8): 
            return 1.0
        elif mes in (10, 5, 11): 
            return 0.9
        else:
            return 1.0  

    def buscar_paquete(self, paquete_id):
        paquete_objeto = self._repo.read_by_id(paquete_id)
        if not paquete_objeto:
            raise ValueError("Paquete turístico no encontrado")
        
        lista_destinos = self._repo_destino.get_all_destinos(paquete_id)
        paquete_objeto.destinos = lista_destinos
        return paquete_objeto
    
    def agregar_paquete(self, paquete):
        self._repo.create(paquete)
        return paquete
    def agregar_destino_a_paquete(self, paquete, destino):
        orden_visita = self._repo.get_ultimo_orden_visita(paquete.id_paquete) + 1
        destino.orden_visita = orden_visita
        multiplicador = self.obtener_multiplicador(paquete.fecha_salida)
        self._repo.destino_x_paquete(paquete,destino)
        if destino.pais != "Chile":
            paquete.modalidad = "Internacional"
            self._repo.update(paquete)
        if orden_visita > 1:
            paquete.fecha_llegada = destino.fecha_llegada
            self._repo.update(paquete)

    def confirmar_fecha_salida(self, fecha, fecha_salida = None):
        hoy = date.today()
            
        fecha_limite = hoy + timedelta(days=7)
        if fecha_salida != None and fecha < fecha_salida:
            return "Error! No puede ingresar una fecha anterior a la fecha de inicio del paquete."
        if fecha < fecha_limite:
            return "Error! Solo se pueden ingresar fechas con 7 dias de antelacion."
        else:
            return True

    def confirmar_fecha_llegada(self, fecha_llegada, fecha_salida ):
        if fecha_salida < fecha_llegada:
            return True
        else:
            return "Error! La fecha de llegada no puede ser anterior a la fecha de Salida. "
        
    def duplicidad_verf(self, destino_id,paquete_id):
        return self._repo.duplicidad_destino(destino_id,paquete_id)
    
    def quitar_paquete(self, id_paquete):
        return self._repo.eliminar_paquete(id_paquete)

    def quitar_destino(self,id_paquete, orden_visita):
        destino = self._repo.obtener_destino(id_paquete, orden_visita)
        fecha_inicio = destino['fecha_salida']
        fecha_fin = destino['fecha_llegada']
        diferencia = fecha_fin - fecha_inicio
        diferencia_dias = diferencia.days
        self._repo.eliminar_destino(id_paquete, orden_visita, diferencia_dias)


    def traer_paquetes(self, tipo):
        if tipo == 1:
            modalidad = "Nacional"
        else:
            modalidad = "Internacional"
        lista_paquetes = self._repo.traer_paquetes(modalidad)
        return lista_paquetes
    

    def verificar_cupos(self, id_paquete, cupos):
        paquete = self._repo.read_by_id(id_paquete)
        if cupos > paquete.cupos:
            return False
        return True
    
    def obtener_todos(self):
        paquetes = self._repo.get_all()
        for p in paquetes:
            p.destinos = self._repo_destino.get_all_destinos(p.id_paquete)
        return paquetes
