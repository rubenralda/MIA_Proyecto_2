from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .usuario import is_sesion, valor_usuario
from .mount import obtener_particiones

class Mkgrp(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        name = self.parametros.get("name")
        if name == None:
            print("--Error: Faltan parametros--")
            return False
        if not is_sesion():
            print("--Error: no hay una sesion abierta--")
            return False
        usuario = valor_usuario()
        if usuario.nombre_user != "root":
            print("--Error: requere permisos de usuario root--")
            return False
        id_particion = usuario.id_particion
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id_particion:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    archivo_binario.seek(particion.start)
                    superbloque = SuperBloque(0,0,0)
                    superbloque.set_bytes(archivo_binario)
                    superbloque.agregar_grupo_userstxt(archivo_binario, name)
                    archivo_binario.seek(particion.start)
                    archivo_binario.write(superbloque.get_bytes())
                    print("\n--Grupo agregado--\n")
                    return True