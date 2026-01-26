from src.Datos.reserva_repository import Reservas_Repository
from src.Logica_de_Negocio.models.Reserva import Reserva

class Reservas_Service:
    def __init__(self, reserva_repository: Reservas_Repository):
        self._repo = reserva_repository

    def crear_reserva(self, datos_reserva, id_usuario, id_paquete):
        nueva_reserva = Reserva(
            id_usuario = id_usuario,
            estado = datos_reserva['estado'],
            cupos = datos_reserva["cupos"]
        )
        print(nueva_reserva)
        return self._repo.create(nueva_reserva, id_usuario,id_paquete)
    
    def obtener_reserva_por_id(self, id_reserva):
        reserva = self._repo.read_by_id(id_reserva)
        return reserva
    
    def actualizar_reserva(self, reserva_objeto):
        if reserva_objeto.estado not in ["pendiente", "confirmada", "cancelada"]:
            raise ValueError("Estado inválido para la reserva.")
        
        if reserva_objeto.monto_total <= 0:
            raise ValueError("El monto total debe ser mayor a 0.")
        
        if reserva_objeto.fecha_inicio >= reserva_objeto.fecha_final:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha final.")
        
        return self._repo.update(reserva_objeto)

    
    def eliminar_reserva(self, id_reserva):
        return self._repo.delete(id_reserva)
    
    def obtener_reservas_por_usuario(self, id_usuario):
        return self._repo.read_by_usuario(id_usuario)

    def obtener_todas_reservas(self):
        return self._repo.read_all()