from .comando_base import Comando
from .usuario import cerrar_sesion

class Logout(Comando):
    
    def ejecutar(self):
        if cerrar_sesion():
            return "--Sesion cerrada--\n"
        return "Error: no hay una sesion abierta\n"