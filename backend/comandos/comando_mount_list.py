from .comando_base import Comando
from .mount import obtener_particiones

class MountList(Comando):

    def __init__(self) -> None:
        super().__init__()
    
    def ejecutar(self):
        particiones = obtener_particiones()
        for particion in particiones:
            print("ID:", particion.id, "Tipo:", particion.tipo_particion, "Nombre:", particion.nombre)