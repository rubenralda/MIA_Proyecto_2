from .comando_base import Comando
from .estructuras.estructura_mbr import Mbr
from .estructuras.estructura_particion import Particion
from .mount import agregar_particion
import os

class Mount(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        path_particion = self.parametros.get("path")
        name = self.parametros.get("name")
        if path_particion == None or name == None:
            print("--Error: Faltan parametros--")
            return False
        if not os.path.isfile(path_particion):
            print("--Error: El disco no existe--")
            return False
        with open(path_particion, "rb+") as archivo_binario: #Recupero los valores de mbr
            estruct_mbr = Mbr(0, 0, 0, 0)
            estruct_mbr.set_bytes(archivo_binario) # valores del mbr recuperados
            particion = estruct_mbr.buscar_particion(name, archivo_binario)
            if particion == None:
                print("--Error: La particion no existe--")
                return False
            tipo_clase = "L"
            size = 0
            start = 0
            if isinstance(particion, Particion):
                if particion.tipo == "E":
                    print("--Error: No se puede montar una particion extendida--")
                    return False
                tipo_clase = "P"
                size = particion.s
                start = particion.start
            else:
                size = particion.size - 30 # 30 del size de ebr
                start = particion.start + 30 # 30 despues del ebr
            agregar_particion(particion, path_particion, tipo_clase, name, size, start, archivo_binario)
            print("\n--Particion agregada--\n")
