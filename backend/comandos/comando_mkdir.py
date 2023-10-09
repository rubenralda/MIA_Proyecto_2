from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .usuario import valor_usuario
from .mount import obtener_particiones

class Mkdir(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        path = self.parametros.get("path")
        if path == None:
            return "Error: Faltan parametros\n"
        r = self.parametros.get("r", False)
        usuario = valor_usuario()
        if usuario ==  None:
            return "Error: inicia sesion antes\n"
        id_particion = usuario.id_particion
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id_particion:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    archivo_binario.seek(particion.start)
                    superbloque = SuperBloque(0,0,0)
                    superbloque.set_bytes(archivo_binario)
                    creacion = superbloque.crear_carpeta(archivo_binario, path, r, int(usuario.id_user), int(usuario.id_grupo))
                    if creacion["status"]:
                        # escribir los cambios del superbloque
                        archivo_binario.seek(particion.start)
                        archivo_binario.write(superbloque.get_bytes())
                    return creacion["mensaje"]
        return "Error: la particion no ha sido montada\n"