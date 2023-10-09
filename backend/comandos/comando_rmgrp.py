from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .usuario import is_sesion, valor_usuario
from .mount import obtener_particiones

class Rmgrp(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros
    
    def ejecutar(self):
        name = self.parametros.get("name")
        if name == None:
            return "Error: Faltan parametros\n"
        if not is_sesion():
            return "Error: no hay una sesion abierta\n"
        usuario = valor_usuario()
        if usuario.nombre_user != "root":
            return "Error: requere permisos de usuario root\n"
        id_particion = usuario.id_particion
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id_particion:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    archivo_binario.seek(particion.start)
                    superbloque = SuperBloque(0,0,0)
                    superbloque.set_bytes(archivo_binario)
                    if not superbloque.eliminar_grupo_userstxt(archivo_binario, name):
                        return "Error: el nombre de grupo no existe\n"
                    archivo_binario.seek(particion.start)
                    archivo_binario.write(superbloque.get_bytes())
                    return "--Grupo Eliminado--\n"
        return "Error: particion no encontrada\n"