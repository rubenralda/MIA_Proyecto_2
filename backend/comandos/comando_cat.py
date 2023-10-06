from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .usuario import valor_usuario
from .mount import obtener_particiones

class Cat(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        path = self.parametros.get("file1")
        if path == None:
            print("--Error: Faltan parametros--")
            return False
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
                    for file in range(len(self.parametros)):
                        path = self.parametros.get("file" + str(file + 1))
                        if path == None:
                            print("--Error: el parametro no es valido")
                            return False
                        if superbloque.mostrar_archivo(archivo_binario, path, int(usuario.id_user), int(usuario.id_grupo)):
                            continue
                        print("--Error: No se pudo leer el archivo--")
                        return False