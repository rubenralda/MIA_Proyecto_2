from .estructura_base import EstructuraBase
from .estructura_particion import Particion
from .estructura_ebr import Ebr
import time

class Mbr(EstructuraBase):

    def __init__(self, tamano: int, fecha: int, signature: int, fit: str) -> None:
        self.tamano = tamano  # 4 bytes
        self.fecha = fecha  # 4 bytes
        self.signature = signature  # 4 bytes
        self.fit = fit  # 1 byte
        particion1 = Particion("F", "P", "W", 121, 0, "")
        particion2 = Particion("F", "P", "W", 121, 0, "")
        particion3 = Particion("F", "P", "W", 121, 0, "")
        particion4 = Particion("F", "P", "W", 121, 0, "")
        self.particiones = [particion1, particion2,
                            particion3, particion4]  # array mas facil

    def set_bytes(self, archivo_binario):
        bytes = archivo_binario.read(13)
        self.tamano = int.from_bytes(bytes[0:4], byteorder='big')
        self.fecha = int.from_bytes(bytes[4:8], byteorder='big')
        self.signature = int.from_bytes(bytes[8:12], byteorder='big')
        self.fit = bytes[12:13].decode("utf-8")
        for particion in self.particiones:
            particion.set_bytes(archivo_binario)

    # Particion si existe, None si no
    def buscar_particion(self, name: str, archivo_binario):
        largo_nombre = len(name)
        while(largo_nombre < 16):
            name += "\0"
            largo_nombre += 1
        for particion in self.particiones:
            if particion.status == "V":
                if particion.name == name:
                    return particion

        # buscar en las particiones logicas
        for particion in self.particiones:
            if particion.status == "V":
                if particion.tipo == "E":
                    return particion.buscar_particion_logica(name, archivo_binario)
        return None

    # Verifica si ya existe solo hay una extendida y ejecuta el fit del disco
    def crear_particion(self, size: int, name: str, tipo: str, fit: str, archivo_binario):
        if tipo == "L":  # Logica
            for particion in self.particiones:
                if particion.status == "V":
                    if particion.tipo == "E":
                        particion_logica = Ebr(True, fit, 0, size, -1, name)
                        return particion.crear_particion_logica(archivo_binario, particion_logica)
            print("--Error: No hay particion extendida--")
            return False
        else:  # particion Extendidia o primaria
            if tipo == "E": # verifico si no existe ya una
                for particion in self.particiones:
                    if particion.status == "V":
                        if particion.tipo == "E":
                            print("--Error: Ya existe una particion extendida--")
                            return False
            if self.fit == "F":  # firt fit
                return self.crear_particion_ff(size, name, tipo, fit, archivo_binario)
            elif self.fit == "B":  # best fit
                return self.crear_particion_bf(size, name, tipo, fit, archivo_binario)
            elif self.fit == "W":  # worst fit
                return self.crear_particion_wf(size, name, tipo, fit, archivo_binario)
            return False

    # Crea una particion con primer ajuste (first fit)
    def crear_particion_ff(self, size_particion: int, name_particion: str, tipo_particion: str, fit_particion: str, archivo_binario):
        start = 121  # tamaño del mbr bytes 121 pero cuenta desde 0 asi que cuando escribo 121 el indice es 120, por lo tanto inicio en el indice 121
        largo_nombre = len(name_particion)
        while (largo_nombre < 16):
            name_particion += "\0"
            largo_nombre += 1
        nueva_particion = Particion("V", tipo_particion, fit_particion, start, size_particion, name_particion)
        for indice_particion in range(4):
            if self.particiones[indice_particion].status == "F":
                try:
                    for resto in range(indice_particion, 4):
                        if self.particiones[resto].status == "V":
                            if self.particiones[resto].start <= start + size_particion:
                                raise
                            nueva_particion.start = start
                            if tipo_particion == "E":
                                nueva_particion.crear_extendida(archivo_binario)
                            self.particiones[indice_particion] = nueva_particion
                            print("\n--Particion creada--\n")
                            return True
                    if start + size_particion <= self.tamano: # por si es la ultima particion
                        nueva_particion.start = start
                        if tipo_particion == "E":
                            nueva_particion.crear_extendida(archivo_binario)
                        self.particiones[indice_particion] = nueva_particion
                        print("\n--Particion creada--\n")
                        return True
                except:
                    continue
            start += self.particiones[indice_particion].s
        print("--Error: no hay espacio para crear la particion E o P--") 
        return False
    
    # Crear particion con el mejor ajuste (Best Fit)
    def crear_particion_bf(self, size_particion: int, name_particion: str, tipo_particion: str, fit_particion: str, archivo_binario):
        start = 121  # tamaño del mbr bytes 121 pero cuenta desde 0 asi que cuando escribo 121 el indice es 120, por lo tanto inicio en el indice 121
        largo_nombre = len(name_particion)
        while (largo_nombre < 16):
            name_particion += "\0"
            largo_nombre += 1
        espacios = []
        nueva_particion = Particion("V", tipo_particion, fit_particion, start, size_particion, name_particion)
        for indice_particion in range(4):
            if self.particiones[indice_particion].status == "F":
                try:
                    for resto in range(indice_particion, 4):
                        if self.particiones[resto].status == "V":
                            # validar para que se corran las particiones, es decir una particion 2 pueda ir despues de la 4
                            if self.particiones[resto].start <= start + size_particion:
                                raise
                            nuevo_espacio = {
                                "tamano": self.particiones[resto].start - start,
                                "indice_particion" : indice_particion,
                                "inicio" : start
                            }
                            espacios.append(nuevo_espacio)
                            raise
                    if start + size_particion <= self.tamano: # por si es la ultima particion
                        nuevo_espacio = {
                            "tamano": self.tamano - start,
                            "indice_particion" : indice_particion,
                            "inicio" : start
                        }
                        espacios.append(nuevo_espacio)
                        break
                    print("--Error: La particion es muy grande--")
                    return False
                except:
                    continue
            start += self.particiones[indice_particion].s
        # Ahora con los espacios libres guardados vemos el mas pequeño de todos
        if len(espacios) == 0:
            print("--Error: no hay espacio para crear la particion E o P--")
            return False
        espacio_short = espacios[0]
        for espaciolibre in espacios:
            if espaciolibre["tamano"] < espacio_short["tamano"]:
                espacio_short = espaciolibre
        nueva_particion.start = espacio_short["inicio"]
        if tipo_particion == "E":
            nueva_particion.crear_extendida(archivo_binario)
        self.particiones[espacio_short["indice_particion"]] = nueva_particion
        print("\n--Particion creada--\n")
        return True
    
    # Crear particion con el peor ajuste (worst Fit)
    def crear_particion_wf(self, size_particion: int, name_particion: str, tipo_particion: str, fit_particion: str, archivo_binario):
        start = 121  # tamaño del mbr bytes 121 pero cuenta desde 0 asi que cuando escribo 121 el indice es 120, por lo tanto inicio en el indice 121
        largo_nombre = len(name_particion)
        while (largo_nombre < 16):
            name_particion += "\0"
            largo_nombre += 1
        espacios = []
        nueva_particion = Particion("V", tipo_particion, fit_particion, start, size_particion, name_particion)
        for indice_particion in range(4):
            if self.particiones[indice_particion].status == "F":
                try:
                    for resto in range(indice_particion, 4):
                        if self.particiones[resto].status == "V":
                            if self.particiones[resto].start <= start + size_particion:
                                raise
                            nuevo_espacio = {
                                "tamano": self.particiones[resto].start - start,
                                "indice_particion" : indice_particion,
                                "inicio" : start
                            }
                            espacios.append(nuevo_espacio)
                            raise
                    if start + size_particion <= self.tamano: # por si es la ultima particion
                        nuevo_espacio = {
                            "tamano": self.tamano - start,
                            "indice_particion" : indice_particion,
                            "inicio" : start
                        }
                        espacios.append(nuevo_espacio)
                        break
                    print("--Error: La particion es muy grande--")
                    return False
                except:
                    continue
            start += self.particiones[indice_particion].s
        # Ahora con los espacios libres guardados vemos el mas grande de todos
        if len(espacios) == 0:
            print("--Error: no hay espacio para crear la particion E o P--")
            return False
        espacio__grande = espacios[0]
        for espaciolibre in espacios:
            if espaciolibre["tamano"] > espacio__grande["tamano"]:
                espacio__grande = espaciolibre
        nueva_particion.start = espacio__grande["inicio"]
        if tipo_particion == "E":
            nueva_particion.crear_extendida(archivo_binario)
        self.particiones[espacio__grande["indice_particion"]] = nueva_particion
        print("\n--Particion creada--\n")
        return True
    
    # True si fue exitoso, False si no
    def eliminar_particion(self, name: str, archivo_binario):
        largo_nombre = len(name)
        while(largo_nombre < 16):
            name += "\0"
            largo_nombre += 1
        i = 0
        for particion in self.particiones:
            if particion.status == "V":
                if particion.name == name:
                    particion.status = "F"
                    archivo_binario.seek(particion.start)
                    archivo_binario.write(b'\x00'*particion.s)
                    particion.tipo = "P"
                    return True
            i += 1
        for particion in self.particiones:
            if particion.status == "V":       
                if particion.tipo == "E":
                    return particion.eliminar_particion_logica(name, archivo_binario)
        return False
    
    # True si existe, False si no
    def add_particion(self, name: str, archivo_binario, add: int):
        largo_nombre = len(name)
        while(largo_nombre < 16):
            name += "\0"
            largo_nombre += 1
        for i, particion in enumerate(self.particiones):
            if particion.status == "V":
                if particion.name == name:
                    nuevo_size = particion.s + add
                    if nuevo_size < 0:
                        return False
                    elif i == 3:
                        if nuevo_size > self.tamano:
                            return False
                    else:
                        if nuevo_size >= self.particiones[i+1].start:
                            return False
                    self.particiones[i].s = nuevo_size
                    return True
                
        # buscar en las particiones logicas
        for i, particion in enumerate(self.particiones):
            if particion.status == "V":
                if particion.tipo == "E":
                    return particion.add_particion_logica(name, archivo_binario, add)
        return False
    
    def reporte_mbr(self, archivo_binario) -> str:
        reporte = '''digraph reporte_del_mbr_ff {{
    node [shape=plaintext]
    mbr [
        label=<
            <table border="0" cellborder="1" cellspacing="0">
                <tr>
                <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b>REPORTE DE MBR</b></td>
                <td bgcolor="/rdylgn6/5:/rdylgn6/5"><b> </b></td>
                </tr>
                <tr>
                <td>mbr_tamano</td><td>{}</td>
                </tr>
                <tr>
                <td>mbr_fecha_creacion</td><td>{}</td>
                </tr>
                <tr>
                <td>mbr_disk_signature</td><td>{}</td>
                </tr>'''.format(self.tamano, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.fecha)), self.signature)
        for particion in self.particiones:
            reporte += particion.reporte_particion(archivo_binario)
        reporte += '''</table>
        >];
}'''
        return reporte
    
    def reporte_disk(self, archivo_binario) -> str:
        reporte = '''digraph reporte_del_disk {
    node [shape=plaintext]
    disk_f [
        label=<
            <table border="0" cellborder="1" cellspacing="0">
                <tr>
                    <td bgcolor="/rdylgn6/5:/rdylgn6/5" rowspan="2"><b>MBR</b></td>
                '''
        logicas = ""

        start = 121
        todo_libre = True
        if self.particiones[0].status == "F":
            for resto in range(1, 4):
                if self.particiones[resto].status == "V":
                    porcentaje_libre = (self.particiones[resto].start - start) / self.tamano
                    reporte += '''<td rowspan="2">Libre1<BR/>{}%</td>'''.format(str(porcentaje_libre*100))
                    todo_libre = False
                    break
            if todo_libre:
                porcentaje_libre = 100
                reporte += '''<td rowspan="2">Libre2<BR/>{}%</td>'''.format(str(porcentaje_libre*100))
                reporte += '''</tr>'''
                reporte += logicas
                reporte += '''</table>
                >];
                }'''
                return reporte
        for indice_particion in range(4):
            
            if self.particiones[indice_particion].status == "V":
                if self.particiones[indice_particion].tipo == "E":
                    result = self.particiones[indice_particion].reporte_disk(archivo_binario, self.tamano)
                    reporte += result["fila"]
                    logicas = result["extendida"]
                else:
                    porcentaje_primaria = self.particiones[indice_particion].s / self.tamano
                    reporte += '''<td rowspan="2">Primaria<BR/>{}%</td>'''.format(str(porcentaje_primaria*100))
                try:
                    for resto in range(indice_particion + 1, 4):
                        if self.particiones[resto].status == "V":
                            if self.particiones[resto].start - (self.particiones[indice_particion].start + self.particiones[indice_particion].s) != 0:
                                porcentaje_libre = (self.particiones[resto].start - (self.particiones[indice_particion].start + self.particiones[indice_particion].s)) / self.tamano
                                reporte += '''<td rowspan="2">Libre3<BR/>{}%</td>'''.format(str(porcentaje_libre*100))
                            raise
                    porcentaje_libre = (self.tamano - (self.particiones[indice_particion].start + self.particiones[indice_particion].s)) / self.tamano
                    reporte += '''<td rowspan="2">Libre4<BR/>{}%</td>'''.format(str(porcentaje_libre*100))
                    break
                except:
                    start += self.particiones[indice_particion].s
                    continue
        reporte += '''</tr>'''
        reporte += logicas
        reporte += '''</table>
        >];
        }'''
        return reporte