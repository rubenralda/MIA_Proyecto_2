from .comando_base import Comando
from .mount import eliminar_montada

class Unmount(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        id = self.parametros.get("id")
        if id == None:
            print("--Error: Faltan parametros--")
            return False
        if eliminar_montada(id):
            print("\n--Particion desmontada--\n")
            return True
        print("--Error: la particion no ha sido montada o no existe--")
        return False
        