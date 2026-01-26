class Destino():
    def __init__(self,
                nombre,
                ciudad,
                pais,
                descripcion,
                actividades_disponibles,
                orden_visita = None,
                fecha_llegada = None,
                fecha_salida = None,
                id_destino = None):

        self.id_destino = id_destino
        self.nombre = nombre
        self.ciudad = ciudad
        self.pais = pais
        self.descripcion = descripcion
        self.actividades_disponibles = actividades_disponibles
        self.orden_visita = orden_visita
        self.fecha_salida = fecha_llegada
        self.fecha_llegada = fecha_salida

    def __str__(self):
        return (
        f"Destino: {self.nombre} (ID: {self.id_destino})\n"
        f"Descripción: {self.descripcion}\n"
        f"Actividades disponibles:{self.actividades_disponibles}\n"
        )
    
    def to_dict(self):
        return {
            "id_destino": self.id_destino,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "pais": self.pais,
            "descripcion": self.descripcion,
            "actividades_disponibles": self.actividades_disponibles
        }
    
