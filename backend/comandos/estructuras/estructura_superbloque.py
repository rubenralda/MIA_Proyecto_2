from .estructura_base import EstructuraBase
from .estructura_bloques import *
from .estructura_tabla_inodos import *
from .estructura_journaling import Journaling
from math import floor, ceil
import time,os, random

tamano_journaling = 400

class SuperBloque(EstructuraBase):

    def __init__(self, filesystem: int, start: int, size: int) -> None:
        self.filesystem_type = filesystem # 4 bytes int, 0 = ext2 y  1 = ext3
        n = (size - 68) / (tamano_journaling*filesystem + 4 + 92 + 3*64) # si es ext3 se suma el size del journaling
        numero_structuras = floor(n)

        self.inodos_count = numero_structuras # 4 bytes int
        self.bloque_count = numero_structuras * 3  # 4 bytes int
        self.inodos_libres_count = numero_structuras # 4 bytes int
        self.bloque_libres_count = numero_structuras * 3  # 4 bytes int

        self.tiempo_montado = 0 # 4 bytes int
        self.tiempo_desmontado = 0 # 4 bytes int
        self.conteo_montadas = 0 # 4 bytes int
        
        self.magic = 61299 # 4 bytes int 0xEF53
        self.tamano_inodo = 92 # 4 bytes int
        self.tamano_bloque = 64 # 4 bytes int

        self.primer_inodo_libre = 2 # 4 bytes int
        self.primer_bloque_libre = 2 # 4 bytes int
        self.bitmap_inodo_start = start + 68 + tamano_journaling*self.filesystem_type*numero_structuras # 4 bytes int
        self.bitmap_bloque_start = self.bitmap_inodo_start + numero_structuras # 4 bytes int
        self.inodo_start = self.bitmap_bloque_start + 3*numero_structuras# 4 bytes int
        self.bloque_start = self.inodo_start + numero_structuras*self.tamano_inodo # 4 bytes int

    def set_bytes(self, archivo_binario=None):
        bytes = archivo_binario.read(68)
        self.filesystem_type = int.from_bytes(bytes[0:4], byteorder = 'big')
        self.inodos_count = int.from_bytes(bytes[4:8], byteorder = 'big')
        self.bloque_count = int.from_bytes(bytes[8:12], byteorder = 'big')
        self.inodos_libres_count = int.from_bytes(bytes[12:16], byteorder = 'big')
        self.bloque_libres_count = int.from_bytes(bytes[16:20], byteorder = 'big')
        self.tiempo_montado = int.from_bytes(bytes[20:24], byteorder = 'big')
        self.tiempo_desmontado = int.from_bytes(bytes[24:28], byteorder = 'big')
        self.conteo_montadas = int.from_bytes(bytes[28:32], byteorder = 'big')
        self.magic = int.from_bytes(bytes[32:36], byteorder = 'big')
        self.tamano_inodo = int.from_bytes(bytes[36:40], byteorder = 'big')
        self.tamano_bloque = int.from_bytes(bytes[40:44], byteorder = 'big')
        self.primer_inodo_libre = int.from_bytes(bytes[44:48], byteorder = 'big')
        self.primer_bloque_libre = int.from_bytes(bytes[48:52], byteorder = 'big')
        self.bitmap_inodo_start = int.from_bytes(bytes[52:56], byteorder = 'big')
        self.bitmap_bloque_start = int.from_bytes(bytes[56:60], byteorder = 'big')
        self.inodo_start = int.from_bytes(bytes[60:64], byteorder = 'big')
        self.bloque_start = int.from_bytes(bytes[64:68], byteorder = 'big')

    def archivo_userstxt(self, archivo_binario):
        archivo_binario.seek(self.inodo_start)
        inodo_restaurado = Inodos()
        inodo_restaurado.set_bytes(archivo_binario) # inodo raiz
        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[0]*self.tamano_bloque) 
        carpeta_restaurada = BloqueCarpetas() # carpeta raiz
        carpeta_restaurada.set_bytes(archivo_binario)
        numero_inodo = carpeta_restaurada.buscar("users.txt")
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_archivo = Inodos()
        inodo_archivo.set_bytes(archivo_binario) # inodo raiz
        usuario = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
        inodo_archivo.atime = int(time.time())
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        archivo_binario.write(inodo_archivo.get_bytes())
        return usuario
    
    def agregar_grupo_userstxt(self, archivo_binario, nombre_grupo: str):
        archivo_binario.seek(self.inodo_start)
        inodo_restaurado = Inodos()
        inodo_restaurado.set_bytes(archivo_binario) # inodo raiz
        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[0]*self.tamano_bloque) 
        carpeta_restaurada = BloqueCarpetas() # carpeta raiz
        carpeta_restaurada.set_bytes(archivo_binario)
        numero_inodo = carpeta_restaurada.buscar("users.txt")
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_archivo = Inodos()
        inodo_archivo.set_bytes(archivo_binario) # inodo raiz
        contenido = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
        if contenido == None:
            print("--Error: error muy inesperado--")
        lineas = contenido.split("\n")[:-1]
        id = 1
        for linea in lineas:
            items = linea.split(",")
            if items[1] == "G": #es grupo
                id += 1
                continue
        contenido += str(id) + ",G,"+ nombre_grupo + "\n"
        # escribir de nuevo el contenido
        self.guardar_operacion("MKGRP", contenido, "/users.txt", archivo_binario)
        return self.escribir_cambios_userstxt(archivo_binario, inodo_archivo, numero_inodo, contenido)

    def eliminar_grupo_userstxt(self, archivo_binario, nombre_grupo: str):
        archivo_binario.seek(self.inodo_start)
        inodo_restaurado = Inodos()
        inodo_restaurado.set_bytes(archivo_binario) # inodo raiz
        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[0]*self.tamano_bloque) 
        carpeta_restaurada = BloqueCarpetas() # carpeta raiz
        carpeta_restaurada.set_bytes(archivo_binario)
        numero_inodo = carpeta_restaurada.buscar("users.txt")
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_archivo = Inodos()
        inodo_archivo.set_bytes(archivo_binario) # inodo raiz
        contenido = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
        if contenido == None:
            print("--Error: error muy inesperado--")
        lineas = contenido.split("\n")[:-1]
        nuevo_contenido = ""
        cambiado = False
        for linea in lineas:
            items = linea.split(",")
            if items[1] == "G" and items[0] != "0": #es grupo
                if items[2] == nombre_grupo:
                    items[0] = "0"
                    cambiado = True
                    nuevo_contenido += items[0] + "," + items[1] + "," + items[2] + "\n"
                    continue
            nuevo_contenido += linea + "\n"
        if not cambiado:
            print("--Error: el nombre de grupo no existe--")
            return False
        # escribir de nuevo el contenido
        self.guardar_operacion("RMGRP", nuevo_contenido, "/users.txt", archivo_binario)
        return self.escribir_cambios_userstxt(archivo_binario, inodo_archivo, numero_inodo, nuevo_contenido)

    def agregar_usuario_userstxt(self, archivo_binario, nombre_usuario: str, contra:str, nombre_grupo:str):
        archivo_binario.seek(self.inodo_start)
        inodo_restaurado = Inodos()
        inodo_restaurado.set_bytes(archivo_binario) # inodo raiz
        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[0]*self.tamano_bloque) 
        carpeta_restaurada = BloqueCarpetas() # carpeta raiz
        carpeta_restaurada.set_bytes(archivo_binario)
        numero_inodo = carpeta_restaurada.buscar("users.txt")
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_archivo = Inodos()
        inodo_archivo.set_bytes(archivo_binario) # inodo raiz
        contenido = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
        if contenido == None:
            print("--Error: error muy inesperado--")
        lineas = contenido.split("\n")[:-1]
        id = 1
        existe_grupo = False
        for linea in lineas:
            items = linea.split(",")
            if items[1] == "U": #es usuario
                id += 1
            elif items[2] == nombre_grupo:
                    existe_grupo = True
        if not existe_grupo:
            print("--Error: el grupo no existe--")
            return False
        contenido += str(id) + ",U,"+ nombre_grupo + "," + nombre_usuario + "," + contra + "\n"
        # escribir de nuevo el contenido
        self.guardar_operacion("MKUSR", contenido, "/users.txt", archivo_binario)
        return self.escribir_cambios_userstxt(archivo_binario, inodo_archivo, numero_inodo, contenido)

    def eliminar_usuario_userstxt(self, archivo_binario, nombre_usuario: str):
        archivo_binario.seek(self.inodo_start)
        inodo_restaurado = Inodos()
        inodo_restaurado.set_bytes(archivo_binario) # inodo raiz
        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[0]*self.tamano_bloque) 
        carpeta_restaurada = BloqueCarpetas() # carpeta raiz
        carpeta_restaurada.set_bytes(archivo_binario)
        numero_inodo = carpeta_restaurada.buscar("users.txt")
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_archivo = Inodos()
        inodo_archivo.set_bytes(archivo_binario) # inodo raiz
        contenido = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
        if contenido == None:
            print("--Error: error muy inesperado--")
        lineas = contenido.split("\n")[:-1]
        nuevo_contenido = ""
        cambiado = False
        for linea in lineas:
            items = linea.split(",")
            if items[1] == "U" and items[0] != "0": #es usuario
                if items[3] == nombre_usuario:
                    items[0] = "0"
                    cambiado = True
                    nuevo_contenido += items[0] + "," + items[1] + "," + items[2] + "," + items[3] + "," + items [4] + "\n"
                    continue
            nuevo_contenido += linea + "\n"
        if not cambiado:
            print("--Error: el nombre de usuario no existe--")
            return False
        # escribir de nuevo el contenido
        self.guardar_operacion("RMUSR", nuevo_contenido, "/users.txt", archivo_binario)
        return self.escribir_cambios_userstxt(archivo_binario, inodo_archivo, numero_inodo, nuevo_contenido)
    
    def escribir_cambios_userstxt(self, archivo_binario,  inodo_archivo: Inodos, numero_inodo:int, nuevo_contenido:str):
        self.primer_bloque_libre = inodo_archivo.bloque[0]
        for i in range(12): # apuntadores directos
            if inodo_archivo.bloque[i] != -1:
                archivo_binario.seek(self.bitmap_bloque_start + inodo_archivo.bloque[i])
                archivo_binario.write(bytes([0]))
                self.bloque_libres_count += 1
        # agregar apuntadores indirectos !
        size = len(nuevo_contenido)
        inodo_archivo.size = size # numero de caracteres
        indice_bloque = 0
        while size >= 64:
            size -= 64
            parte_contenido = nuevo_contenido[0:64]
            nuevo_contenido = nuevo_contenido[64:]
            parte_archivo = BloqueArchivos(parte_contenido)
            archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
            archivo_binario.write(parte_archivo.get_bytes())
            inodo_archivo.bloque[indice_bloque] = self.primer_bloque_libre
            indice_bloque += 1
            self.utilizar_un_bloque(archivo_binario)
        if size != 0:
            parte_archivo = BloqueArchivos(nuevo_contenido)
            archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
            archivo_binario.write(parte_archivo.get_bytes())
            inodo_archivo.bloque[indice_bloque] = self.primer_bloque_libre
            self.utilizar_un_bloque(archivo_binario)
        inodo_archivo.mtime = int(time.time())
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        archivo_binario.write(inodo_archivo.get_bytes())
        return True
        
    def crear_carpeta(self, archivo_binario, path: str, r:bool, id_usuario, id_grpo):
        # seek en posicion despues del superbloque
        path_split = path.split("/")
        carpetas = path_split[1:]
        nombre_carpeta = carpetas[-1]
        carpetas = carpetas[:-1]
        numero_inodo = 0
        for x, carpeta in enumerate(carpetas):
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            if inodo_restaurado.tipo != 0:
                print("--Error: no es carpeta")
                return False
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        numero_inodo = carpeta_restaurada.buscar(carpeta)
                        if numero_inodo != -1:
                            raise
                # agregar aqui los apuntadores indirectos
            except:
                continue
            # si llego aqui no encontro nada
            if r:
                numero_inodo = self.primer_inodo_libre
                self.crear_carpeta(archivo_binario, "/".join(path_split[:x + 2]), True, id_usuario, id_grpo)
                continue
            print("--Error: La ruta no existe--")
            return False
        # tengo el numero de inodo_carpeta que contendra la nueva carpeta
        # creo el inodo archivo
        inodo_carpeta = Inodos()
        inodo_carpeta.uid = id_usuario
        inodo_carpeta.gid = id_grpo
        inodo_carpeta.size = 0
        inodo_carpeta.atime = int(time.time())
        inodo_carpeta.ctime = int(time.time())
        inodo_carpeta.mtime= int(time.time())
        inodo_carpeta.tipo = 0 # carpeta
        inodo_carpeta.permiso = 664
        # busco donde insertar
        numero_contenedor = numero_inodo # guardar la posicion
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_carpeta_contenedor = Inodos()
        inodo_carpeta_contenedor.set_bytes(archivo_binario)
        posicion_bloque_contenedor = -1 # puntero bloque proximo
        posicion_libre_carpeta = -1 # posicion vacia del bloque carpeta
        posicion_libre_bloque = -1 # puntero al bloque con una posicion vacia
        # busco si existe
        for i in range(12):
            if inodo_carpeta_contenedor.bloque[i] != -1:
                archivo_binario.seek(self.bloque_start + inodo_carpeta_contenedor.bloque[i]*self.tamano_bloque) 
                carpeta_restaurada = BloqueCarpetas()
                carpeta_restaurada.set_bytes(archivo_binario)
                posicion_libre_carpeta = carpeta_restaurada.posicion_vacia()
                if posicion_libre_carpeta != -1:
                    posicion_libre_bloque = i
            elif posicion_bloque_contenedor == -1:
                posicion_bloque_contenedor = i #primer vacio que encuentre
        if posicion_libre_bloque != -1:
            archivo_binario.seek(self.bloque_start + inodo_carpeta_contenedor.bloque[posicion_libre_bloque]*self.tamano_bloque)
            carpeta_padre = BloqueCarpetas()
            carpeta_padre.set_bytes(archivo_binario)
            contenido = ContenidoCarpeta(nombre_carpeta, self.primer_inodo_libre)
            carpeta_padre.contenido[posicion_libre_carpeta] = contenido
            archivo_binario.seek(self.bloque_start + inodo_carpeta_contenedor.bloque[posicion_libre_bloque]*self.tamano_bloque)
            archivo_binario.write(carpeta_padre.get_bytes())
            self.escribir_carpeta(archivo_binario, inodo_carpeta, self.primer_inodo_libre)
            self.guardar_operacion("MKDIR", "--", path, archivo_binario)
            return True
        elif posicion_bloque_contenedor != -1: # crear un nuevo bloque de carpetas
            carpeta_nueva = BloqueCarpetas()
            contenido = ContenidoCarpeta(nombre_carpeta, self.primer_inodo_libre)
            carpeta_nueva.contenido[0] = contenido
            archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
            archivo_binario.write(carpeta_nueva.get_bytes())
            # escribir el cambio en el inodo
            inodo_carpeta_contenedor.bloque[posicion_bloque_contenedor] = self.primer_bloque_libre
            archivo_binario.seek(self.inodo_start + numero_contenedor*self.tamano_inodo)
            archivo_binario.write(inodo_carpeta_contenedor.get_bytes())
            self.utilizar_un_bloque(archivo_binario)
            self.escribir_carpeta(archivo_binario, inodo_carpeta, self.primer_inodo_libre)
            self.guardar_operacion("MKDIR", "--", path, archivo_binario)
            return True
        return False

    def escribir_carpeta(self, archivo_binario, inodo_carpeta: Inodos, numero_inodo: int):
        carpeta_nueva = BloqueCarpetas()
        contenido_padre = ContenidoCarpeta(".", numero_inodo)
        contenido_propio = ContenidoCarpeta("..", 0)
        carpeta_nueva.contenido[0] = contenido_padre
        carpeta_nueva.contenido[1] = contenido_propio
        archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
        archivo_binario.write(carpeta_nueva.get_bytes())
        inodo_carpeta.bloque[0] = self.primer_bloque_libre
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        archivo_binario.write(inodo_carpeta.get_bytes())
        self.utilizar_un_bloque(archivo_binario)
        self.utilizar_un_inodo(archivo_binario)

    def crear_archivo(self, archivo_binario, size: int, path: str, r:bool, id_usuario, id_grpo, cont_copia: str):
        # seek en posicion despues del superbloque, bitmap inician desde 0
        if size == 0:
            bloques_archivo = 1
        else:
            bloques_archivo = ceil(size / self.tamano_bloque) #numero de bloques
        if bloques_archivo >= self.bloque_libres_count:
            print("--Error: La particion esta llena--")
        path_split = os.path.dirname(path).split("/")
        carpetas = path_split[1:] # path.split("/")[1:]
        nombre_archivo = os.path.basename(path)
        numero_inodo = 0
        for x, carpeta in enumerate(carpetas):
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            if inodo_restaurado.tipo != 0:
                print("--Error: no es carpeta")
                return False
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        numero_inodo = carpeta_restaurada.buscar(carpeta)
                        if numero_inodo != -1:
                            raise
                # agregar aqui los apuntadores indirectos
            except:
                continue
            # si llego aqui no encontro nada
            if r:
                numero_inodo = self.primer_inodo_libre
                self.crear_carpeta(archivo_binario, "/".join(path_split[:x + 2]), True, id_usuario, id_grpo)
                continue
            print("--Error: La ruta no existe--")
            return False
        # tengo el numero de inodo_carpeta que contiene o no el archivo a escribir
        # creo el inodo archivo
        inodo_archivo = Inodos()
        inodo_archivo.uid = id_usuario
        inodo_archivo.gid = id_grpo
        inodo_archivo.size = size
        inodo_archivo.atime = int(time.time())
        inodo_archivo.ctime = int(time.time())
        inodo_archivo.mtime= int(time.time())
        inodo_archivo.tipo = 1 # archivo
        inodo_archivo.permiso = 664
        # busco donde insertar
        existe = False
        numero_contenedor = numero_inodo # guardar la posicion
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_carpeta_contenedor = Inodos()
        inodo_carpeta_contenedor.set_bytes(archivo_binario)
        posicion_bloque_contenedor = -1 # puntero bloque proximo
        posicion_libre_carpeta = -1 # posicion vacia del bloque carpeta
        posicion_libre_bloque = -1 # puntero al bloque con una posicion vacia
        # busco si existe
        for i in range(12):
            if inodo_carpeta_contenedor.bloque[i] != -1:
                archivo_binario.seek(self.bloque_start + inodo_carpeta_contenedor.bloque[i]*self.tamano_bloque) 
                carpeta_restaurada = BloqueCarpetas()
                carpeta_restaurada.set_bytes(archivo_binario)
                numero_inodo = carpeta_restaurada.buscar(nombre_archivo) # buscar si esta el archivo
                if numero_inodo != -1: # ya existe por lo tanto hay que sobreescribir
                    posicion_bloque_contenedor = i #bloque que encontro
                    existe = True
                    break
                posicion_libre_carpeta = carpeta_restaurada.posicion_vacia()
                if posicion_libre_carpeta != -1:
                    posicion_libre_bloque = i
            elif posicion_bloque_contenedor == -1:
                posicion_bloque_contenedor = i #primer vacio que encuentre
        if existe:
            print("Desea sobreecribir los datos? y/n")
            respuesta = input(">:")
            if respuesta.lower() == "y":
                # numero_inodo es posicion del antiguo bloque
                # logica para borrar el archivo
                pass
            else:
                return False
        if posicion_libre_bloque != -1:
            archivo_binario.seek(self.bloque_start + inodo_carpeta_contenedor.bloque[posicion_libre_bloque]*self.tamano_bloque)
            carpeta_del_archivo = BloqueCarpetas()
            carpeta_del_archivo.set_bytes(archivo_binario)
            contenido = ContenidoCarpeta(nombre_archivo, self.primer_inodo_libre)
            carpeta_del_archivo.contenido[posicion_libre_carpeta] = contenido
            archivo_binario.seek(self.bloque_start + inodo_carpeta_contenedor.bloque[posicion_libre_bloque]*self.tamano_bloque)
            archivo_binario.write(carpeta_del_archivo.get_bytes())
            if cont_copia != "":
                archivo = cont_copia
            else:
                caracteres = "0123456789"
                archivo = "".join(random.choice(caracteres) for _ in range(size))
            self.escribir_archivo(archivo_binario, inodo_archivo, self.primer_inodo_libre, archivo)
            self.guardar_operacion("MKFILE", archivo, path, archivo_binario)
            return True
        elif posicion_bloque_contenedor != -1: # crear un nuevo bloque de carpetas
            carpeta_nueva = BloqueCarpetas()
            contenido = ContenidoCarpeta(nombre_archivo, self.primer_inodo_libre)
            carpeta_nueva.contenido[0] = contenido
            archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
            archivo_binario.write(carpeta_nueva.get_bytes())
            # escribir el cambio en el inodo
            inodo_carpeta_contenedor.bloque[posicion_bloque_contenedor] = self.primer_bloque_libre
            archivo_binario.seek(self.inodo_start + numero_contenedor*self.tamano_inodo)
            archivo_binario.write(inodo_carpeta_contenedor.get_bytes())
            self.utilizar_un_bloque(archivo_binario)
            if cont_copia != "":
                archivo = cont_copia
            else:
                caracteres = "0123456789"
                archivo = "".join(random.choice(caracteres) for _ in range(size))
            self.escribir_archivo(archivo_binario, inodo_archivo, self.primer_inodo_libre, archivo)
            self.guardar_operacion("MKFILE", archivo, path, archivo_binario)
            return True
        return False
    
    def escribir_archivo(self, archivo_binario,  inodo_archivo: Inodos, numero_inodo:int, nuevo_contenido:str):
        size = len(nuevo_contenido)
        inodo_archivo.size = size # numero de caracteres
        indice_bloque = 0
        if size != 0:
            while size >= 64:
                size -= 64
                parte_contenido = nuevo_contenido[0:64]
                nuevo_contenido = nuevo_contenido[64:]
                parte_archivo = BloqueArchivos(parte_contenido)
                archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
                archivo_binario.write(parte_archivo.get_bytes())
                inodo_archivo.bloque[indice_bloque] = self.primer_bloque_libre
                indice_bloque += 1
                self.utilizar_un_bloque(archivo_binario)
            if size != 0:
                parte_archivo = BloqueArchivos(nuevo_contenido)
                archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
                archivo_binario.write(parte_archivo.get_bytes())
                inodo_archivo.bloque[indice_bloque] = self.primer_bloque_libre
                self.utilizar_un_bloque(archivo_binario)
        else:
            parte_archivo = BloqueArchivos(nuevo_contenido)
            archivo_binario.seek(self.bloque_start + self.primer_bloque_libre*self.tamano_bloque)
            archivo_binario.write(parte_archivo.get_bytes())
            inodo_archivo.bloque[indice_bloque] = self.primer_bloque_libre
            self.utilizar_un_bloque(archivo_binario)
        inodo_archivo.mtime = int(time.time())
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        archivo_binario.write(inodo_archivo.get_bytes())
        self.utilizar_un_inodo(archivo_binario)
        return True

    def mostrar_archivo(self, archivo_binario, path: str, id_usuario: int, id_grpo: int):
        # seek en posicion despues del superbloque
        carpetas = path.split("/") #os.path.dirname(path).split("/")[1:]
        numero_inodo = 0
        for carpeta in carpetas:
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            if inodo_restaurado.tipo != 0:
                print("--Error: no es carpeta")
                return False
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        numero_inodo = carpeta_restaurada.buscar(carpeta)
                        if numero_inodo != -1:
                            raise
            except:
                continue
            # si llego aqui no encontro las rutas
            print("--Error: La ruta no existe--")
            return False
        if numero_inodo != -1:
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_archivo = Inodos()
            inodo_archivo.set_bytes(archivo_binario)
            contenido_archivo = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
            print("#", contenido_archivo)
            self.guardar_operacion("CAT", "--", path, archivo_binario)
            return True
        return False

    def remove(self, archivo_binario, path: str, id_usuario, id_grpo):
        # seek en posicion despues del superbloque
        path_split = path.split("/")
        carpetas = path_split[1:]
        numero_inodo = 0
        numero_bloque_contenedor_borrar = -1
        posicion_contenido_bloque = -1
        for x, carpeta in enumerate(carpetas):
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            if inodo_restaurado.tipo != 0:
                print("--Error: no es carpeta")
                return False
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        tamano = len(carpeta)
                        while tamano < 12:
                            carpeta += "\0"
                            tamano += 1
                        for m, contenido in enumerate(carpeta_restaurada.contenido):
                            if contenido.name == carpeta:
                                numero_inodo = contenido.inodo
                                if x == len(carpetas) -1:
                                    posicion_contenido_bloque = m
                                    numero_bloque_contenedor_borrar = inodo_restaurado.bloque[i]
                                raise
                # agregar aqui los apuntadores indirectos
            except:
                continue
            print("--Error: La ruta no existe--")
            return False
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_borrar = Inodos()
        inodo_borrar.set_bytes(archivo_binario)
        if inodo_borrar.tipo == 1: #archivo
            for i in range(12):
                if inodo_borrar.bloque[i] != -1:
                    archivo_binario.seek(self.bitmap_bloque_start + inodo_borrar.bloque[i])
                    archivo_binario.write(bytes([0]))
                    self.primer_bloque_libre = inodo_borrar.bloque[i] # con suerte queda antes y puede llenar los siguientes eliminados
        else: # carpeta 
            for i in range(12):
                if inodo_borrar.bloque[i] != -1:
                    archivo_binario.seek(self.bloque_start + inodo_borrar.bloque[i]*self.tamano_bloque) 
                    carpeta_eliminar = BloqueCarpetas()
                    carpeta_eliminar.set_bytes(archivo_binario)
                    for m, contenido in enumerate(carpeta_eliminar.contenido):
                        if contenido.name.replace("\0", "") == "." or contenido.name.replace("\0", "") == "..":
                            continue
                        if contenido.inodo == -1:
                            continue
                        self.remove(archivo_binario, path + "/" + carpeta_eliminar.contenido[m].name.replace("\0", ""), id_usuario, id_grpo)
                    archivo_binario.seek(self.bitmap_bloque_start + inodo_borrar.bloque[i])
                    archivo_binario.write(bytes([0]))
        archivo_binario.seek(self.bitmap_inodo_start + numero_inodo)
        archivo_binario.write(bytes([0]))

        archivo_binario.seek(self.bloque_start + numero_bloque_contenedor_borrar*self.tamano_bloque) 
        carpeta_restaurada = BloqueCarpetas()
        carpeta_restaurada.set_bytes(archivo_binario)
        nuevo_contenido = ContenidoCarpeta("", -1)
        carpeta_restaurada.contenido[posicion_contenido_bloque] = nuevo_contenido
        archivo_binario.seek(self.bloque_start + numero_bloque_contenedor_borrar*self.tamano_bloque)
        archivo_binario.write(carpeta_restaurada.get_bytes())
        self.guardar_operacion("REMOVE", "--", path, archivo_binario)
        return True

    def editar_archivo(self, archivo_binario, path: str, id_usuario, id_grpo, cont_copia: str):
        # seek en posicion despues del superbloque, bitmap inician desde 0
        path_split = path.split("/")
        carpetas = path_split[1:]
        numero_inodo = 0
        for x, carpeta in enumerate(carpetas):
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        numero_inodo = carpeta_restaurada.buscar(carpeta)
                        if numero_inodo != -1:
                            raise
                # agregar aqui los apuntadores indirectos
            except:
                continue
            print("--Error: La ruta no existe--")
            return False
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo) #numero_inodo es el inodo archivo
        inodo_archivo = Inodos()
        inodo_archivo.set_bytes(archivo_binario)
        inodo_archivo.mtime = int(time.time())
        self.primer_bloque_libre = inodo_archivo.bloque[0]
        for i in range(12):
            if inodo_archivo.bloque[i] != -1:
                archivo_binario.seek(self.bitmap_bloque_start + inodo_archivo.bloque[i]) 
                archivo_binario.write(bytes([0]))
                inodo_archivo.bloque[i] = -1
        self.escribir_archivo(archivo_binario, inodo_archivo, numero_inodo, cont_copia)
        self.guardar_operacion("EDIT", cont_copia, path, archivo_binario)
        return True
    
    def editar_nombre(self, archivo_binario, path: str, id_usuario, id_grpo, nombre: str):
        # seek en posicion despues del superbloque, bitmap inician desde 0
        path_split = path.split("/")
        carpetas = path_split[1:]
        numero_inodo = 0
        for x, carpeta in enumerate(carpetas):
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        tamano = len(carpeta)
                        while tamano < 12:
                            carpeta += "\0"
                            tamano += 1
                        for m, contenido in enumerate(carpeta_restaurada.contenido):
                            if contenido.name == carpeta:
                                numero_inodo = contenido.inodo
                                if x == len(carpetas) -1:
                                    nuevo_contenido = ContenidoCarpeta(nombre, carpeta_restaurada.contenido[m].inodo)
                                    carpeta_restaurada.contenido[m] = nuevo_contenido
                                    archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque)
                                    archivo_binario.write(carpeta_restaurada.get_bytes())
                                raise
                # agregar aqui los apuntadores indirectos
            except:
                continue
            print("--Error: La ruta no existe--")
            return False
        self.guardar_operacion("RENAME", nombre, path, archivo_binario)
        return True

    def utilizar_un_bloque(self, archivo_binario): 
        # actualizar el bitmap de bloques
        archivo_binario.seek(self.bitmap_bloque_start + self.primer_bloque_libre) # estoy en el byte libre
        archivo_binario.write(bytes([1])) # indico que esta ocupado
        for i in range(self.bitmap_bloque_start + self.primer_bloque_libre + 1, self.inodo_start): # busco el siguiente libre
            es_vacio = not bool(int.from_bytes(archivo_binario.read(1)[0:1], byteorder= 'big'))
            if es_vacio:
                #archivo_binario.seek(-1, 1) # regreso al que lei
                #archivo_binario.write(bytes([1]))
                self.primer_bloque_libre = i  - self.bitmap_bloque_start # obtengro el valor del bloque
                self.bloque_libres_count -= 1 # resto el nuevo bloque
                break

    def utilizar_un_inodo(self, archivo_binario):
        # actualizar el bitmap de inodos
        archivo_binario.seek(self.bitmap_inodo_start + self.primer_inodo_libre) # estoy en el byte libre
        archivo_binario.write(bytes([1])) # indico que esta ocupado
        for i in range(self.bitmap_inodo_start + self.primer_inodo_libre + 1, self.bitmap_bloque_start): # busco el siguiente libre
            es_vacio = not bool(int.from_bytes(archivo_binario.read(1)[0:1], byteorder= 'big'))
            if es_vacio:
                #archivo_binario.seek(-1, 1) # regreso al que lei
                #archivo_binario.write(bytes([1]))
                self.primer_inodo_libre = i  - self.bitmap_inodo_start # obtengro el nuevo inodo libre
                self.inodos_libres_count -= 1 # resto el nuevo inodo
                break

    def guardar_operacion(self, operacion:str, contenido: str, path: str, archivo_binario):
        if self.filesystem_type == 0:
            return
        inicio = self.bitmap_inodo_start - tamano_journaling*self.inodos_count
        archivo_binario.seek(inicio)
        primer_journaling = Journaling("", "", "")
        primer_journaling.set_bytes(archivo_binario)

        nuevo_entrada = Journaling(operacion, path, contenido)
        archivo_binario.seek(inicio + tamano_journaling*primer_journaling.conteo)
        archivo_binario.write(nuevo_entrada.get_bytes())

        # actualizar el primero
        archivo_binario.seek(inicio)
        primer_entrada = Journaling("", "", "")
        primer_entrada.set_bytes(archivo_binario)
        primer_entrada.conteo += 1
        archivo_binario.seek(inicio)
        archivo_binario.write(primer_entrada.get_bytes())

    def reporte_sb(self):
        fileSystem = "EXT2"
        if self.filesystem_type == 1:
            fileSystem = "EXT3"
        reporte = '''digraph reporte_del_mbr_ff {{
    node [shape=plaintext]
    mbr [
        label=<
            <table border="0" cellborder="1" cellspacing="0">
                <tr>
                    <td bgcolor="/rdylgn6/5:/rdylgn6/5" COLSPAN="2"><b>REPORTE DE SUPERBLOQUE</b></td>
                </tr>
                <tr>
                    <td>File System type</td><td>{}</td>
                </tr>
                <tr>
                    <td>Cantidad i-nodos</td><td>{}</td>
                </tr>
                <tr>
                    <td>Cantidad bloques</td><td>{}</td>
                </tr>
                <tr>
                    <td>Cantidad i-nodos libres</td><td>{}</td>
                </tr>
                <tr>
                    <td>Cantidad bloques libres</td><td>{}</td>
                </tr>
                <tr>
                    <td>Ultimo montaje</td><td>{}</td>
                </tr>
                <tr>
                    <td>Ultimo desmontaje</td><td>{}</td>
                </tr>
                <tr>
                    <td>Conteo montajes</td><td>{}</td>
                </tr>
                <tr>
                    <td>Magic</td><td>{}</td>
                </tr>
                <tr>
                    <td>Tamano i-nodo</td><td>{}</td>
                </tr>
                <tr>
                    <td>Tamano bloque</td><td>{}</td>
                </tr>
                <tr>
                    <td>Primer i-nodo libre</td><td>{}</td>
                </tr>
                <tr>
                    <td>Primer bloque libre</td><td>{}</td>
                </tr>
                <tr>
                    <td>Inicio Bitmap de i-nodos</td><td>{}</td>
                </tr>
                <tr>
                    <td>Inicio Bitmap de bloques</td><td>{}</td>
                </tr>
                <tr>
                    <td>Inicio de i-nodos</td><td>{}</td>
                </tr>
                <tr>
                    <td>Inicio de bloques</td><td>{}</td>
                </tr>'''.format(fileSystem, str(self.inodos_count), str(self.bloque_count), str(self.inodos_libres_count),
                                str(self.bloque_libres_count), time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.tiempo_montado)),
                                time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.tiempo_desmontado)), str(self.conteo_montadas),
                                str(self.magic), str(self.tamano_inodo), str(self.tamano_bloque), str(self.primer_inodo_libre),
                                str(self.primer_bloque_libre), str(self.bitmap_inodo_start), str(self.bitmap_bloque_start),
                                str(self.inodo_start), str(self.bloque_start))
        reporte += '''</table>
            >];
        }'''
        return reporte
    
    def reporte_bm_inodo(self, archivo_binario):
        reporte = ""
        archivo_binario.seek(self.bitmap_inodo_start)
        i = 1
        for _ in range(self.bitmap_inodo_start, self.bitmap_bloque_start):
            valor = str(int.from_bytes(archivo_binario.read(1)[0:1], byteorder= 'big'))
            reporte += valor
            if i % 20 == 0:
                reporte += "\n"
            i += 1
        return reporte
    
    def reporte_bm_bloc(self, archivo_binario):
        reporte = ""
        archivo_binario.seek(self.bitmap_bloque_start)
        i = 1
        for _ in range(self.bitmap_bloque_start, self.inodo_start):
            valor = str(int.from_bytes(archivo_binario.read(1)[0:1], byteorder= 'big'))
            reporte += valor
            if i % 20 == 0:
                reporte += "\n"
            i += 1
        return reporte
    
    def reporte_inodos(self, archivo_binario):
        reporte = '''digraph G {
            rankdir=LR
            node [shape=box]'''
        conexion = "Inicio"
        archivo_binario.seek(self.bitmap_inodo_start)
        i = 0
        for _ in range(self.bitmap_inodo_start, self.bitmap_bloque_start):
            activo = bool(int.from_bytes(archivo_binario.read(1)[0:1], byteorder= 'big'))
            if activo:
                posicion_orginal = archivo_binario.tell()
                archivo_binario.seek(self.inodo_start + (i*self.tamano_inodo))
                inodo_restaurado = Inodos()
                inodo_restaurado.set_bytes(archivo_binario)
                reporte += inodo_restaurado.reporte_inodo(i)
                conexion += " -> "+ str(i)
                archivo_binario.seek(posicion_orginal)
            i += 1
        reporte += conexion
        reporte += '}'
        return reporte
    
    def reporte_bloques(self, archivo_binario):
        reporte = '''digraph B {
            rankdir=LR
            node [shape=box]'''
        conexion = "Inicio"
        archivo_binario.seek(self.bitmap_inodo_start)
        i = 0
        for _ in range(self.bitmap_inodo_start, self.bitmap_bloque_start):
            activo = bool(int.from_bytes(archivo_binario.read(1)[0:1], byteorder= 'big'))
            if activo:
                posicion_orginal = archivo_binario.tell()
                archivo_binario.seek(self.inodo_start + (i*self.tamano_inodo))
                inodo_restaurado = Inodos()
                inodo_restaurado.set_bytes(archivo_binario)
                resultado = inodo_restaurado.reporte_bloque(self.bloque_start, self.tamano_bloque, archivo_binario)
                reporte += resultado["reporte"]
                conexion += resultado["conexion"]
                archivo_binario.seek(posicion_orginal)
            i += 1
        reporte += conexion
        reporte += '}'
        return reporte

    def reporte_arbol(self, archivo_binario):
        reporte = '''digraph G {
            rankdir=LR
            node [fontsize = "16" shape = "ellipse"]'''
        resultado = self.reporte_arbol_base(archivo_binario, 0)
        reporte += resultado["nodos"]
        reporte += resultado["conexion"]
        reporte += '}'
        return reporte
    
    def reporte_arbol_base(self, archivo_binario, numero_inodo):
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo = Inodos()
        inodo.set_bytes(archivo_binario)
        if inodo.tipo == 1: #archivo
            return self.reporte_arbol_archivo(archivo_binario, numero_inodo)
        else:
            return self.reporte_arbol_carpeta(archivo_binario, numero_inodo)

    def reporte_arbol_archivo(self, archivo_binario, numero_inodo):
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo = Inodos()
        inodo.set_bytes(archivo_binario)
        reporte = "nodo" + str(numero_inodo) +'[label="<f0>Inodo ' + str(numero_inodo) + ' | {Tipo |' + str(inodo.tipo) + '}' + ' | {Size |' + str(inodo.size) + '}'
        conexion = "nodo" + str(numero_inodo) + ':f0;\n'
        nodos_bloque = ""
        for i in range(12):
            reporte += ' | {ap' + str(i) + ' | <f' + str(i+1) + '>' + str(inodo.bloque[i]) + '}'
            if inodo.bloque[i] != -1:
                archivo_binario.seek(self.bloque_start + inodo.bloque[i]*self.tamano_bloque)
                archivo = BloqueArchivos("")
                archivo.set_bytes(archivo_binario)
                nodos_bloque += "bloque" + str(inodo.bloque[i]) +'[label="<f0>Bloque Archivo ' + str(inodo.bloque[i]) + ' | <f1> ' + archivo.contenido.replace("\0", "") + '" shape = "record"];\n'
                conexion += 'nodo' + str(numero_inodo) + ':f' + str(i+1) + ' -> ' + "bloque" + str(inodo.bloque[i]) + ':f0;\n'
        reporte += '" shape = "record"];\n'
        reporte += nodos_bloque
        return {"nodos" : reporte, "conexion": conexion}
    
    def reporte_arbol_carpeta(self, archivo_binario, numero_inodo):
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo = Inodos()
        inodo.set_bytes(archivo_binario)
        reporte = "nodo" + str(numero_inodo) +'[label="<f0>Inodo ' + str(numero_inodo) + ' | {Tipo |' + str(inodo.tipo) + '}'  + ' | {Size |' + str(inodo.size) + '}'
        conexion = "nodo" + str(numero_inodo) + ':f0;\n'
        nodos = ""
        nodos_bloque = ""
        for i in range(12):
            reporte += ' | {ap' + str(i) + ' | <f' + str(i+1) + '>' + str(inodo.bloque[i]) + '}'
            if inodo.bloque[i] != -1:
                archivo_binario.seek(self.bloque_start + inodo.bloque[i]*self.tamano_bloque)
                carpeta = BloqueCarpetas()
                carpeta.set_bytes(archivo_binario)
                nodos_bloque += "bloque" + str(inodo.bloque[i]) +'[label="<f0>Bloque carpeta ' + str(inodo.bloque[i])
                conexion += 'nodo' + str(numero_inodo) + ':f' + str(i+1) + ' -> ' + "bloque" + str(inodo.bloque[i]) + ':f0;\n'
                for j, content in enumerate(carpeta.contenido):
                    nodos_bloque += ' | {' + content.name.replace("\0", "") + ' | ' + '<f' + str(j+1) + '>' + str(content.inodo) + '}'
                    if content.inodo != -1:
                        if content.name.replace("\0", "") == "." or content.name.replace("\0", "") == "..":
                            continue
                        resultado = self.reporte_arbol_base(archivo_binario, content.inodo)
                        nodos += resultado["nodos"]
                        conexion += "bloque" + str(inodo.bloque[i]) + ':f' + str(j+1) + ' -> ' + resultado["conexion"]
                nodos_bloque += '" shape = "record"];\n'
        reporte += '" shape = "record"];\n'
        reporte += nodos
        reporte += nodos_bloque
        return {"nodos" : reporte, "conexion": conexion}

    def reporte_file(self, archivo_binario, path: str):
        # seek en posicion despues del superbloque
        carpetas = path.split("/") #os.path.dirname(path).split("/")[1:]
        numero_inodo = 0
        for carpeta in carpetas:
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            if inodo_restaurado.tipo != 0:
                print("--Error: no es carpeta")
                return
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        numero_inodo = carpeta_restaurada.buscar(carpeta)
                        if numero_inodo != -1:
                            raise
            except:
                continue
            # si llego aqui no encontro las rutas
            print("--Error: La ruta no existe--")
            return
        if numero_inodo != -1:
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_archivo = Inodos()
            inodo_archivo.set_bytes(archivo_binario)
            contenido_archivo = inodo_archivo.restaurar_archivo(self.bloque_start, self.tamano_bloque, archivo_binario)
            return contenido_archivo
        return
    
    def reporte_ls(self, archivo_binario, path: str):
        # seek en posicion despues del superbloque
        reporte = '''digraph reporte_del_mbr_ff {
        node [shape=plaintext]
        mbr [
            label=<
                <table border="0" cellborder="1" cellspacing="0">
                    <tr>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Permisos</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Propietario</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Grupo</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Size(bytes)</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Fecha</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Tipo</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Name</b></td>
                    </tr>
        '''
        path_split = path.split("/")
        carpetas = path_split[1:]
        numero_inodo = 0
        for x, carpeta in enumerate(carpetas):
            if carpeta == "":
                continue
            archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
            inodo_restaurado = Inodos()
            inodo_restaurado.set_bytes(archivo_binario)
            try:
                for i in range(12):
                    if inodo_restaurado.bloque[i] != -1:
                        archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                        carpeta_restaurada = BloqueCarpetas()
                        carpeta_restaurada.set_bytes(archivo_binario)
                        numero_inodo = carpeta_restaurada.buscar(carpeta)
                        if numero_inodo != -1:
                            raise
                # agregar aqui los apuntadores indirectos
            except:
                continue
            print("--Error: La ruta no existe--")
            return False
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo) #numero_inodo es el inodo archivo
        inodo_carpeta = Inodos()
        inodo_carpeta.set_bytes(archivo_binario)
        inodo_carpeta.mtime = int(time.time())
        for i in range(12):
            if inodo_carpeta.bloque[i] != -1:
                archivo_binario.seek(self.bloque_start + inodo_carpeta.bloque[i]*self.tamano_bloque) 
                carpeta_reporte = BloqueCarpetas()
                carpeta_reporte.set_bytes(archivo_binario)
                for contenido in carpeta_reporte.contenido:
                    reporte += self.reporte_ls_ruta(contenido.inodo, archivo_binario, contenido.name.replace("\0", ""))
        reporte += '''</table>
            >];
        }'''
        return reporte
    
    def reporte_ls_ruta(self, numero_inodo: int, archivo_binario, nombre:str):
        reporte = ""
        if numero_inodo == -1 or nombre == "." or nombre== "..":
            return reporte
        archivo_binario.seek(self.inodo_start + numero_inodo*self.tamano_inodo)
        inodo_restaurado = Inodos()
        inodo_restaurado.set_bytes(archivo_binario)
        tipo = "Archivo"
        if inodo_restaurado.tipo == 0:
            tipo = "Carpeta"
        reporte += '''<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>'''.format(str(inodo_restaurado.permiso), str(inodo_restaurado.uid), 
                                str(inodo_restaurado.gid), str(inodo_restaurado.size),
                                time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(inodo_restaurado.mtime)),
                                tipo, nombre)
        if inodo_restaurado.tipo == 0:
            for i in range(12):
                if inodo_restaurado.bloque[i] != -1:
                    archivo_binario.seek(self.bloque_start + inodo_restaurado.bloque[i]*self.tamano_bloque) 
                    carpeta_reporte = BloqueCarpetas()
                    carpeta_reporte.set_bytes(archivo_binario)
                    for contenido in carpeta_reporte.contenido:
                        reporte += self.reporte_ls_ruta(contenido.inodo, archivo_binario, contenido.name.replace("\0", ""))
        return reporte
                        
    def reporte_journaling(self, archivo_binario):
        # seek en posicion despues del superbloque
        reporte = '''digraph reporte_del_mbr_ff {
        node [shape=plaintext]
        mbr [
            label=<
                <table border="0" cellborder="1" cellspacing="0">
                    <tr>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Operacion</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Path</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Contenido</b></td>
                        <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>Fecha</b></td>
                    </tr>
        '''
        if self.filesystem_type == 0:
            print("--Error: el tipo de sistema es ext2--")
            reporte += '''</table>
            >];
        }'''
            return reporte
        inicio = self.bitmap_inodo_start - tamano_journaling*self.inodos_count
        archivo_binario.seek(inicio)
        primer_journaling = Journaling("", "", "")
        primer_journaling.set_bytes(archivo_binario)
        archivo_binario.seek(inicio) # para tomar en cuenta el primero
        entrada = Journaling("", "", "")
        for i in range(primer_journaling.conteo):
            archivo_binario.seek(inicio + i*tamano_journaling)
            entrada.set_bytes(archivo_binario)
            reporte += '''<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            </tr>'''.format(entrada.tipo_operacion.replace("\0", ""), entrada.path.replace("\0", ""), 
                                    entrada.contenido.replace("\0", ""),
                                    time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(entrada.fecha)))
        reporte += '''</table>
            >];
        }'''
        return reporte