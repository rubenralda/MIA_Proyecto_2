from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .usuario import valor_usuario
from .mount import obtener_particiones
import os

class Mkfile(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        path = self.parametros.get("path")
        if path == None:
            return "Error: Faltan parametros\n"
        size = self.parametros.get("size", 0)
        if size < 0:
            return "Error: el size no puede ser negativo\n"
        r = self.parametros.get("r", False)
        usuario = valor_usuario()
        if usuario == None:
            return "Error: inicia sesion antes\n"
        ruta_cont = self.parametros.get("cont")
        cont = ""
        if ruta_cont != None:
            if not os.path.isfile(ruta_cont):
                return "Error: la ruta de cont no existe\n"
            with open(ruta_cont, "r") as archivo_copiar:
                cont = archivo_copiar.read()
        id_particion = usuario.id_particion
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id_particion:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    archivo_binario.seek(particion.start)
                    superbloque = SuperBloque(0,0,0)
                    superbloque.set_bytes(archivo_binario)
                    creacion = superbloque.crear_archivo(archivo_binario, size, path, r, int(usuario.id_user), int(usuario.id_grupo), cont)
                    if creacion["status"]:
                        # escribir los cambios del superbloque
                        archivo_binario.seek(particion.start)
                        archivo_binario.write(superbloque.get_bytes())
                    return creacion["mensaje"]
        return "Error: la particion no ha sido montada\n"