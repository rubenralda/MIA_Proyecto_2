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
            print("--Error: Faltan parametros")
            return False
        r = self.parametros.get("r", False)
        usuario = valor_usuario()
        if usuario ==  None:
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
                    if superbloque.crear_carpeta(archivo_binario, path, r, int(usuario.id_user), int(usuario.id_grupo)):
                        # escribir los cambios del superbloque
                        archivo_binario.seek(particion.start)
                        archivo_binario.write(superbloque.get_bytes())
                        print("\n--Carpeta creada--\n")
                        return True
                    print("--Error: no se pudo crear la carpeta--")
                    return False