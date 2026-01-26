class Reserva():
    def __init__ (self, 
                estado,
                cupos,
                id_usuario = None,
                id_reserva = None,
                id_paquete_turistico = None):
        
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.cupos = cupos
        self.estado = estado
        self.id_paquete_turistico = id_paquete_turistico
    
    def __str__(self):
        info_reserva = (
            f"Reserva ID: {self.id_reserva}\n"
            f"Usuario ID: {self.id_usuario}\n"
            f"Estado: {self.estado}\n")
        
        return info_reserva

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "id_usuario": self.id_usuario,
            "cupos": self.cupos,
            "estado": self.estado,
            "id_paquete_turistico": self.id_paquete_turistico
        }