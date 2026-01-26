from .models.Destino import Destino

class Destino_Service:
    
    def __init__(self, destino_repository):
        self._repo = destino_repository 

    def obtener_destino_por_nombre(self, nombre_destino):
        destino_objeto = self._repo.read_by_name(nombre_destino)
        return destino_objeto
    def obtener_destino_por_id(self, id_destino):
        destino_objeto = self._repo.read_by_id(id_destino)
        return destino_objeto
    def nuevo_destino(self,registro):
        destino_objeto = Destino(**registro)
        self._repo.create(destino_objeto)
    def eliminar_destino(self,id_destino):
        self._repo.delete(id_destino)
    def modificar_destino(self, destino):
        self._repo.update(destino)
    def obtener_destinos_por_fecha(self, fecha):
        destino_objeto = self._repo.read_by_date()
        return destino_objeto
    def obtener_destinos_por_pais(self, pais):


        lista_destinos = self._repo.get_destinos_pais(pais)



        return lista_destinos

    def obtener_todos(self):
        return self._repo.get_all()
