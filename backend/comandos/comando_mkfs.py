from .estructuras.estructura_tabla_inodos import Inodos
from .estructuras.estructura_bloques import *
from .estructuras.estructura_journaling import Journaling
from .comando_base import Comando
from .estructuras.estructura_superbloque import SuperBloque
from .mount import obtener_particiones
import time

class Mkfs(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        id = self.parametros.get("id")
        if id == None:
            print("--Error: Faltan parametros--")
            return False
        fs = self.parametros.get("fs", "2fs")
        tipo_formateo = self.parametros.get("type", "full") # parece que no se usa
        if tipo_formateo.lower() != "full":
            print("--Error: valor de parametro incorrecto--")
            return False
        file_system = 0 # ext2
        if fs == "3fs":
            file_system = 1 # ext3
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    #print(particion.start, "---------------------")
                    superbloque = SuperBloque(file_system, particion.start, particion.size)
                    superbloque.bloque_libres_count -= 2 # por la carpeta raiz y archivo users.txt
                    superbloque.inodos_libres_count -= 2 # por el inodo raiz y archivo users.txt
                    archivo_binario.seek(particion.start)
                    archivo_binario.write(superbloque.get_bytes())
                    # escribir el journaling si es ext3
                    if file_system == 1:
                        journaling = Journaling("f", "", "")
                        for _ in range(superbloque.inodos_count):
                            archivo_binario.write(journaling.get_bytes())
                    # escribir el bitmap de inodos
                    archivo_binario.seek(superbloque.bitmap_inodo_start) # si es ext3 ya se sumo el size journaling
                    archivo_binario.write(bytes([1,1])) # inodo del root
                    for _ in range(2, superbloque.inodos_count + 1):
                        archivo_binario.write(bytes([0]))
                    # escribir el bitmap de bloques
                    archivo_binario.seek(superbloque.bitmap_bloque_start)
                    archivo_binario.write(bytes([1,1])) # bloque del root
                    for _ in range(2, superbloque.bloque_count + 1):
                        archivo_binario.write(bytes([0]))
                    # escribir los inodos
                    inodos = Inodos()
                    archivo_binario.seek(superbloque.inodo_start)
                    for _ in range(superbloque.inodos_count):
                        archivo_binario.write(inodos.get_bytes())
                    # escribir los blques
                    bloque = BloqueCarpetas()
                    for _ in range(superbloque.bloque_count):
                        archivo_binario.write(bloque.get_bytes())

                    #escribir la carpeta raiz
                    inodo_raiz = Inodos()
                    inodo_raiz.uid = 1
                    inodo_raiz.gid = 1
                    inodo_raiz.size = 0
                    inodo_raiz.atime = int(time.time())
                    inodo_raiz.ctime = int(time.time())
                    inodo_raiz.mtime= int(time.time())
                    inodo_raiz.tipo = 0
                    inodo_raiz.permiso = 600
                    inodo_raiz.bloque[0] = 0 #apunto al bloque carpeta root
                    archivo_binario.seek(superbloque.inodo_start)
                    archivo_binario.write(inodo_raiz.get_bytes())

                    carpeta_root = BloqueCarpetas()
                    contenido_padre = ContenidoCarpeta(".", 0)
                    contenido_propio = ContenidoCarpeta("..", 0)
                    contenido_archivo = ContenidoCarpeta("users.txt", 1)
                    carpeta_root.contenido[0] = contenido_padre
                    carpeta_root.contenido[1] = contenido_propio
                    carpeta_root.contenido[2] = contenido_archivo
                    archivo_binario.seek(superbloque.bloque_start)
                    archivo_binario.write(carpeta_root.get_bytes())
                    
                    #escribir el archivo users
                    usuarios_root = "1,G,root\n1,U,root,root,123\n"
                    inodo_archivo_user = Inodos()
                    inodo_archivo_user.uid = 1
                    inodo_archivo_user.gid = 1
                    inodo_archivo_user.size = len(usuarios_root)
                    inodo_archivo_user.atime = int(time.time())
                    inodo_archivo_user.ctime = int(time.time())
                    inodo_archivo_user.mtime= int(time.time())
                    inodo_archivo_user.tipo = 1 #archivo
                    inodo_archivo_user.permiso = 600
                    inodo_archivo_user.bloque[0] = 1 #apunto al bloque archivo users.txt
                    #print(superbloque.inodo_start, "--------------------------")
                    archivo_binario.seek(superbloque.inodo_start + superbloque.tamano_inodo)
                    archivo_binario.write(inodo_archivo_user.get_bytes())
                    
                    archivo_user = BloqueArchivos(usuarios_root) # bloque 1
                    archivo_binario.seek(superbloque.bloque_start + superbloque.tamano_bloque)
                    archivo_binario.write(archivo_user.get_bytes())
                    print("\n--Formateo completo--\n")
                    return True
        print("--Error: La particion no existe--")
        return False