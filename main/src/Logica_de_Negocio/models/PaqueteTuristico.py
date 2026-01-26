from .Destino import Destino
class PaqueteTuristico():
    def __init__ (self,
                  fecha_salida,
                  fecha_llegada,
                  costo_destino,
                  cupos,
                  modalidad=None,
                  id_paquete = None,
                  destinos = None):
        
        self.fecha_llegada = fecha_llegada
        self.fecha_salida = fecha_salida
        self.costo_destino = costo_destino
        self.id_paquete = id_paquete
        self.modalidad = modalidad
        self.cupos = cupos
        if destinos:
            if isinstance(destinos[0], dict):
                self.destinos = [Destino(**d) for d in destinos] 
            else:
                self.destinos = destinos 
        else:
            self.destinos = []

    def __str__ (self):
        if self.destinos:
            destinos_lineas = []
            for destino in self.destinos:
                linea = f"{destino['nombre']} {destino['ciudad']}, {destino['pais']}"
                destinos_lineas.append(linea)
            
            destinos_str = "\n" + "\n".join(destinos_lineas)
        else:
            destinos_str = " (Sin destinos asignados)"
        costo_formato = f"${self.costo_destino:,.0f}".replace(",", ".")
        
        return (
            f"================================================\n"
            f"PAQUETE TURÍSTICO (ID: {self.id_paquete or 'Nuevo'})\n"
            f"================================================\n"
            f" Modalidad: {self.modalidad or 'N/A'}\n"
            f" Cupos Disponibles: {self.cupos}\n"
            f" Precio Base: {costo_formato}\n"
            f" Periodo: {self.fecha_salida} → {self.fecha_llegada}\n"
            f"\nDestinos en el Itinerario:\n{destinos_str}\n"
            f"================================================\n"
        )
    
    def to_dict(self):
        destinos_list = []
        if self.destinos:
            for d in self.destinos:
                if isinstance(d, dict):
                    destinos_list.append(d)
                elif hasattr(d, 'to_dict'):
                    destinos_list.append(d.to_dict())
                else:
                    destinos_list.append(str(d))
                    
        return {
            "id_paquete": self.id_paquete,
            "fecha_salida": str(self.fecha_salida),
            "fecha_llegada": str(self.fecha_llegada),
            "costo_destino": self.costo_destino,
            "cupos": self.cupos,
            "modalidad": self.modalidad,
            "destinos": destinos_list
        }
