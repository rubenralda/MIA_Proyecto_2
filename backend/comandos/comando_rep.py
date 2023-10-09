from .estructuras.estructura_mbr import Mbr
from .estructuras.estructura_superbloque import SuperBloque
from .comando_base import Comando
from .mount import obtener_particiones
from .reportes import agregar_reportes
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
            return "Error: Faltan parametros\n"
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
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    estruct_mbr = Mbr(0, 0, 0, 0)
                    estruct_mbr.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_mbr.reporte_mbr(archivo_binario)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte mbr creado--\n"
            case "disk":
                particiones = obtener_particiones()
                direccion = ""
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    estruct_mbr = Mbr(0, 0, 0, 0)
                    estruct_mbr.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_mbr.reporte_disk(archivo_binario)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte disk creado--\n"
            case "sb":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_sb()
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte sb creado--\n"
            case "bm_inode":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reportetxt = estruct_sb.reporte_bm_inodo(archivo_binario)
                    with open(path_particion, "w+") as archivo_reporte:
                        archivo_reporte.write(reportetxt)
                agregar_reportes(path_particion)
                return "--Reporte bm_inode creado--\n"
            case "bm_block":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reportetxt = estruct_sb.reporte_bm_bloc(archivo_binario)
                    with open(path_particion, "w+") as archivo_reporte:
                        archivo_reporte.write(reportetxt)
                agregar_reportes(path_particion)
                return "--Reporte bm_block creado--\n"
            case "inode":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_inodos(archivo_binario)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte inode creado--\n"
            case "block":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_bloques(archivo_binario)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte block creado--\n"
            case "tree":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_arbol(archivo_binario)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte tree creado--\n"
            case "file":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    ruta = self.parametros.get("ruta")
                    if ruta == None:
                        return "Error: falta el parametro ruta\n"
                    reportetxt = estruct_sb.reporte_file(archivo_binario, ruta)
                    if reportetxt == None:
                        return "Error: el archivo no existe\n"
                    with open(path_particion, "w+") as archivo_reporte:
                        archivo_reporte.write(reportetxt)
                agregar_reportes(path_particion)
                return "--Reporte file creado--\n"
            case "ls":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    ruta = self.parametros.get("ruta")
                    if ruta == None:
                        return "Error: falta el parametro ruta\n"
                    reporte_graphviz = estruct_sb.reporte_ls(archivo_binario, ruta)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte ls creado--\n"
            case "journaling":
                particiones = obtener_particiones()
                direccion = ""
                inicio = 0
                for particion in particiones:
                    if particion.id == id:
                        direccion = particion.path_disco
                        inicio = particion.start
                if direccion == "":
                    return "Error: El ID no existe para el reporte\n"
                with open(direccion, "rb") as archivo_binario:
                    archivo_binario.seek(inicio)
                    estruct_sb = SuperBloque(0,0,0)
                    estruct_sb.set_bytes(archivo_binario)
                    reporte_graphviz = estruct_sb.reporte_journaling(archivo_binario)
                    #print(reporte_graphviz)
                    # la parte de format es para obtener la extension del archivo
                    grafo = Source(reporte_graphviz, format = extension) # os.path.splitext(os.path.basename(path_particion))[1].replace(".", "")
                    # print(reporte_graphviz)
                    grafo.render(ruta_final)
                agregar_reportes(path_particion)
                return "--Reporte journaling creado--\n"
            case _:
                return "Error: el valor del parametro name es incorrecto\n"
