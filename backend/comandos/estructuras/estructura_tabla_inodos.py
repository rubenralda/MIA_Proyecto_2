from .estructura_base import EstructuraBase
from .estructura_bloques import *
import time

class Inodos(EstructuraBase):

    def __init__(self) -> None:
        self.uid = 1 # 4 int usuario id
        self.gid = 1 # 4 int grupo id
        self.size = 0 # 4 int
        self.atime = int(time.time()) # 4 int
        self.ctime = int(time.time()) # 4 int
        self.mtime = int(time.time()) # 4 int
        self.tipo = 0 # 4 int 1 = archivo y 0 = carpeta
        self.permiso = 0 # 4 int
        self.bloque = [] # 4 * 15 registros int
        for _ in range(15):
            self.bloque.append(-1)
    
    def set_bytes(self, archivo_binario):
        bytes = archivo_binario.read(92)
        self.uid = int.from_bytes(bytes[0:4], byteorder = 'big')
        self.gid = int.from_bytes(bytes[4:8], byteorder = 'big')
        self.size = int.from_bytes(bytes[8:12], byteorder = 'big')
        self.atime = int.from_bytes(bytes[12:16], byteorder = 'big')
        self.ctime = int.from_bytes(bytes[16:20], byteorder = 'big')
        self.mtime = int.from_bytes(bytes[20:24], byteorder = 'big')
        self.tipo = int.from_bytes(bytes[24:28], byteorder = 'big')
        self.permiso = int.from_bytes(bytes[28:32], byteorder = 'big')
        for i in range(15):
            self.bloque[i] = int.from_bytes(bytes[32+4*i:36+4*i], byteorder = 'big', signed= True)
    
    def restaurar_archivo(self, inicio_bloques, tamano_bloque, archivo_binario):
        if self.tipo == 0:
            return None
        contenido = ""
        for i in range(12): # apuntadores directos
            if self.bloque[i] != -1:
                archivo_binario.seek(inicio_bloques + (self.bloque[i]*tamano_bloque))
                bloque_restaurado = BloqueArchivos("")
                bloque_restaurado.set_bytes(archivo_binario)    
                contenido += bloque_restaurado.contenido
        return contenido.replace("\0", "")
    
    def reporte_inodo(self, id: int):
        reporte = str(id) + ''' [label="I-nodo                {}
        Uid                  {}
        Gid                  {}
        Size                 {}
        Fecha de lectura     {}
        Fecha de creacion    {}
        Fecha modificacion   {}
        Tipo                 {}
        Permiso              {}'''.format(str(id), str(self.uid), str(self.gid), str(self.size),
                                        time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.atime)),
                                        time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.ctime)),
                                        time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.mtime)),
                                        str(self.tipo), str(self.permiso))
        for i, bloque in enumerate(self.bloque):
            reporte += "\nBloque" + str(i) + "             " + str(bloque) + ""
        reporte += '"]'
        return reporte
    
    def reporte_bloque(self, inicio_bloques: int, tamano_bloque: int, archivo_binario):
        reporte = ""
        conexion = ""
        if self.tipo == 0:
            for i in range(12):
                if self.bloque[i] != -1:
                    archivo_binario.seek(inicio_bloques + (self.bloque[i]*tamano_bloque))
                    carpeta_restaurada = BloqueCarpetas()
                    carpeta_restaurada.set_bytes(archivo_binario)
                    reporte += carpeta_restaurada.reporte_bloque(self.bloque[i])
                    conexion += " -> " + str(self.bloque[i])
        else: #tipo archivo
            for i in range(12):
                if self.bloque[i] != -1:
                    archivo_binario.seek(inicio_bloques + (self.bloque[i]*tamano_bloque))
                    archivo_restaurado = BloqueArchivos("")
                    archivo_restaurado.set_bytes(archivo_binario)
                    reporte += archivo_restaurado.reporte_bloque(self.bloque[i])
                    conexion += " -> " + str(self.bloque[i])
        return {"reporte" : reporte, "conexion" : conexion}
