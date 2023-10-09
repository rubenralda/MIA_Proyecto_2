from .comando_base import Comando
import os

class Rmdisk(Comando):

    def __init__(self, parametros:dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        direccion = self.parametros.get("path")
        if direccion == None:
            return "Error: Faltan parametros\n"
        if not os.path.isfile(direccion):
            return "Error: La ruta no es un archivo valido\n"
        os.remove(direccion)
        return "--El disco se elimino correctamente--\n"