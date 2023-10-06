from .estructuras.estructura_mbr import Mbr
from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .mount import obtener_particiones
from graphviz import Source
import os

class Rep(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        path_particion = self.parametros.get("path")
        id = self.parametros.get("id")
        name = self.parametros.get("name")
        if path_particion == None or name == None or id == None:
            print("--Error: Faltan parametros--")
            return False
        # Obtenemos el directorio de la ruta (sin el nombre del archivo)
        carpetas = os.path.dirname(path_particion)
        # Verificar si el directorio no existe y crearlo si es necesario
        if not os.path.exists(carpetas):
            os.makedirs(carpetas)
        nombre_divido = os.path.splitext(os.path.basename(path_particion))
        ruta_final = carpetas + "/" + nombre_divido[0]
        extension = nombre_divido[1].replace(".", "")
        match name.lower():
            case "mbr":
                particiones = obtener_particiones()
                direccion = ""
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                if direccion == "":
                    print("--Error: El ID no existe--") 
                    return False
                with open(direccion, "rb") as archivo_binario:
                    estruct_mbr = Mbr(0, 0, 0, 0)
                    estruct_mbr.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_mbr.reporte_mbr(archivo_binario)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
                return True
            case "disk":
                particiones = obtener_particiones()
                direccion = ""
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    estruct_mbr = Mbr(0, 0, 0, 0)
                    estruct_mbr.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_mbr.reporte_disk(archivo_binario)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case "sb":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_sb()
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case "bm_inode":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reportetxt = estruct_sb.reporte_bm_inodo(archivo_binario)
                    with open(path_particion, "w+") as archivo_reporte:
                        archivo_reporte.write(reportetxt)
                    #print(reportetxt)
            case "bm_block":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reportetxt = estruct_sb.reporte_bm_bloc(archivo_binario)
                    with open(path_particion, "w+") as archivo_reporte:
                        archivo_reporte.write(reportetxt)
                    #print(reportetxt) 
            case "inode":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_inodos(archivo_binario)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case "block":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_bloques(archivo_binario)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case "tree":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_arbol(archivo_binario)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case "file":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    ruta = self.parametros.get("ruta")
                    if ruta == None:
                        print("--Error: falta el parametro ruta")
                        return False
                    reportetxt = estruct_sb.reporte_file(archivo_binario, ruta)
                    if reportetxt == None:
                        print("--Error: el archivo no existe")
                        return False
                    with open(path_particion, "w+") as archivo_reporte:
                        archivo_reporte.write(reportetxt)
                        #print(reportetxt)
            case "ls":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    ruta = self.parametros.get("ruta")
                    if ruta == None:
                        print("--Error: falta el parametro ruta")
                        return False
                    reporte_graphviz = estruct_sb.reporte_ls(archivo_binario, ruta)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case "journaling":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    print("--Error: El ID no existe--")
                    return False
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_journaling(archivo_binario)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final, view= True) # falta quitar el .extension porque se pone doble
            case _:
                print("--Error: el valor del parametro name es incorrecto--", name)
                return False
