from .estructura_base import EstructuraBase
import time

class Journaling(EstructuraBase):

    def __init__(self, operacion: str, path: str, contenido: str) -> None: # 400 bytes
        tamano = len(operacion)
        if tamano < 8:
            operacion += "\0"*(8 - tamano)
        tamano = len(path)
        if tamano < 128:
            path += "\0"*(128 - tamano)
        tamano = len(contenido)
        if tamano < 256:
            contenido += "\0"*(256 - tamano)
        self.tipo_operacion = operacion # 8 bytes string
        self.path = path # char 2 bloques * 64 = 128
        self.contenido = contenido # 4 bloques * 64 = 256 
        self.fecha = int(time.time()) # 4 bytes int
        self.conteo = 0 # 4 bytes int

    def set_bytes(self, archivo_binario=None):
        bytes = archivo_binario.read(400)
        self.tipo_operacion = bytes[0:8].decode("utf-8")
        self.path = bytes[8:136].decode("utf-8")
        self.contenido = bytes[136:392].decode("utf-8")
        self.fecha = int.from_bytes(bytes[392:396], byteorder='big')
        self.conteo = int.from_bytes(bytes[396:400], byteorder= 'big')

