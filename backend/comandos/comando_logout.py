from .comando_base import Comando
from .usuario import cerrar_sesion

class Logout(Comando):
    
    def ejecutar(self):
        if cerrar_sesion():
            print("\n--Sesion cerrada--\n")
            return True
        print("--Error: no hay una sesion abierta--")
        return False