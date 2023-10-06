from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .usuario import valor_usuario
from .mount import obtener_particiones

class Rename(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        path = self.parametros.get("path")
        name = self.parametros.get("name")
        if path == None or name == None:
            print("--Error: Faltan parametros--")
            return False
        usuario = valor_usuario()
        if usuario == None:
            print("--Error: inicia sesion antes--")
            return False
        id_particion = usuario.id_particion
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id_particion:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    archivo_binario.seek(particion.start)
                    superbloque = SuperBloque(0,0,0)
                    superbloque.set_bytes(archivo_binario)
                    if superbloque.editar_nombre(archivo_binario, path, int(usuario.id_user), int(usuario.id_grupo), name):
                        # escribir los cambios del superbloque
                        archivo_binario.seek(particion.start)
                        archivo_binario.write(superbloque.get_bytes())
                        print("\n--Nombre cambiado--\n")
                        return True
                    return False
        print("--Error: la particion no ha sido montada--")