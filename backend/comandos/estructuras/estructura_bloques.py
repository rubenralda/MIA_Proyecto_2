from .estructura_base import EstructuraBase

class ContenidoCarpeta(EstructuraBase):

    def __init__(self, name: str, inodo: int) -> None:
        tamano = len(name)
        while tamano < 12:
            name += "\0"
            tamano += 1
        self.name = name # 12 bytes str
        self.inodo = inodo # 4 bytes int apuntador a un inodo asociado al archivo o carpeta
    
    def set_bytes(self, archivo_binario=None):
        bytes = archivo_binario.read(16)
        self.name = bytes[0:12].decode('utf-8')
        self.inodo = int.from_bytes(bytes[12:16], byteorder = 'big', signed= True)

class BloqueCarpetas(EstructuraBase):

    def __init__(self) -> None:
        self.contenido = [ContenidoCarpeta("", -1), ContenidoCarpeta("", -1),
                          ContenidoCarpeta("", -1), ContenidoCarpeta("", -1)]
    
    def set_bytes(self, archivo_binario=None):
        for contenido in self.contenido:
            contenido.set_bytes(archivo_binario)
    
    def reporte_bloque(self, id: int):
        reporte = str(id) + ' [label="Bloque Carpeta {}'.format(str(id)) + '\n' + 'b_name                  b_inodo'
        for contenido in self.contenido:
            reporte += '''\n{}                  {}'''.format(str(contenido.name.replace("\0", "")), str(contenido.inodo))
        reporte += '"]'
        return reporte

    def buscar(self, nombre:str):
        tamano = len(nombre)
        while tamano < 12:
            nombre += "\0"
            tamano += 1
        for contenido in self.contenido:
            if contenido.name == nombre:
                return contenido.inodo
        return -1

    # busca si hay espacio para escribir poner un puntero
    def posicion_vacia(self):
        for i, contenido in enumerate(self.contenido):
            if contenido.inodo == -1:
                return i
        return -1

class BloqueArchivos(EstructuraBase):

    def __init__(self, contenido: str) -> None:
        self.contenido = contenido
        if len(contenido) < 64:
            self.contenido += "\0"*(64-len(contenido))
    
    def set_bytes(self, archivo_binario):
        bytes = archivo_binario.read(64)
        self.contenido = bytes[0:64].decode('utf-8')
    
    def reporte_bloque(self, id: int):
        reporte = str(id) + ' [label="Bloque Archivo {}'.format(str(id)) + '\n'
        reporte += self.contenido.replace("\0", "")
        reporte += '"]'
        return reporte

class BloqueApuntador(EstructuraBase):

    def __init__(self) -> None:
        self.punteros = [-1,-1,-1,-1,
                         -1,-1,-1,-1,
                         -1,-1,-1,-1,
                         -1,-1,-1,-1,
                         ] # 4 bytes int * 16 = 64 bytes
        
    def set_bytes(self, archivo_binario=None):
        return super().set_bytes(archivo_binario)