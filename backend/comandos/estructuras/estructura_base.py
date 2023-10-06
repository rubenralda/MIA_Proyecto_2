from abc import ABC, abstractmethod

class EstructuraBase(ABC):

    def get_bytes(self) -> bytearray:
        bytes = bytearray()
        for atributo, valor in vars(self).items():
            tipo = type(valor).__name__
            if tipo == 'int':
                bytes += valor.to_bytes(4, byteorder = 'big', signed = True)
            elif tipo == 'str':
                bytes += valor.encode('utf-8')
            elif tipo == 'bool':
                bytes += valor.to_bytes(1, byteorder = 'big')
            elif tipo == 'list':
                for item in valor:
                    tipo2 = type(item).__name__
                    if tipo2 == 'int':
                        bytes += item.to_bytes(4, byteorder = 'big', signed = True)
                    elif tipo2 == 'str':
                        bytes += item.encode('utf-8')
                    elif tipo2 == 'bool':
                        bytes += item.to_bytes(1, byteorder = 'big')
                    elif tipo2 == 'list':
                        for item in item:
                            bytes += item.get_bytes()
                    else:
                        bytes += item.get_bytes()
            else:
                bytes += valor.get_bytes()
        return bytes
    
    @abstractmethod
    def set_bytes(self, archivo_binario = None):
        pass