from .estructuras.estructura_superbloque import SuperBloque
import os, time

class Particiones_montadas:

    def __init__(self, id: str, particion, path_disco: str, tipo_particion: str, nombre: str, size: int, start : int) -> None:
        self.particion = particion
        self.path_disco = path_disco
        self.tipo_particion = tipo_particion
        self.id = id
        self.nombre= nombre
        self.size = size
        self.start = start

particion_montadas = []

def obtener_particiones():
    return particion_montadas

def agregar_particion(particion, path_disco:str, tipo: str, nombre: str, size: int, start :int, archivo_binario):
    global particion_montadas
    numero_particion = 1
    for particion in particion_montadas:
        if particion.path_disco == path_disco:
            numero_particion += 1
    id = "35" + str(numero_particion) + os.path.splitext(os.path.basename(path_disco))[0]
    # print(id)
    # actualizo el sistema de ficheros
    archivo_binario.seek(start)
    superbloque = SuperBloque(0,0,0)
    superbloque.set_bytes(archivo_binario)
    superbloque.conteo_montadas += 1
    superbloque.tiempo_montado = int(time.time())
    archivo_binario.seek(start)
    archivo_binario.write(superbloque.get_bytes())
    # monto la particion
    nueva_particion = Particiones_montadas(id, particion, path_disco, tipo, nombre, size, start)
    particion_montadas.append(nueva_particion)
    return True

def eliminar_montada(id: str):
    global particion_montadas
    for i, particion in enumerate(particion_montadas):
        if particion.id == id:
            with open(particion.path_disco, "rb+") as archivo_binario:
                # actualizo el sistema de ficheros
                archivo_binario.seek(particion.start)
                superbloque = SuperBloque(0,0,0)
                superbloque.set_bytes(archivo_binario)
                superbloque.tiempo_desmontado = int(time.time())
                archivo_binario.seek(particion.start)
                archivo_binario.write(superbloque.get_bytes())
            particion_montadas.pop(i)
            return True
    return False