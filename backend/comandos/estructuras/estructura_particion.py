from .estructura_base import EstructuraBase
from .estructura_ebr import Ebr

class Particion(EstructuraBase):

    def __init__(self, status: str, tipo: str, fit: str, start: int, s: int, name: str):
        self.status = status # 1 byte; V si esta activo, F contrario
        self.tipo = tipo # 1 byte
        self.fit = fit # 1 byte
        self.start = start # 4 bytes empieza a contar desde 0
        self.s = s # 4 bytes (size_particion) 
        largo_nombre = len(name)
        while(largo_nombre < 16):
            name += "\0"
            largo_nombre += 1
        self.name = name # 16 bytes
    
    def set_bytes(self, archivo_binario):
        bytes = archivo_binario.read(27)
        self.status = bytes[0:1].decode('utf-8')
        self.tipo = bytes[1:2].decode('utf-8')
        self.fit = bytes[2:3].decode('utf-8')
        self.start = int.from_bytes(bytes[3:7], byteorder = 'big')
        self.s = int.from_bytes(bytes[7:11], byteorder = 'big')
        self.name = bytes[11:27].decode('utf-8')

    def crear_extendida(self, archivo_binario):
        if self.tipo != "E":
            return
        estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
        archivo_binario.seek(self.start)
        archivo_binario.write(estructura_ebr.get_bytes())

    def crear_particion_logica(self, archivo_binario, particion:Ebr):
        if self.tipo != "E":
            return {"status": False, "mensaje": "Error: No se puede crear la particion logica\n"}
        estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
        archivo_binario.seek(self.start)
        estructura_ebr.set_bytes(archivo_binario)
        if not estructura_ebr.status:
            # falta comprobar si despues de eliminar la primera particion que busque si cabe en este espacio
            # por el momento si esta vacia siempre va escribir aqui independiente del fit
            particion.start = self.start
            particion.siguiente = estructura_ebr.siguiente
            archivo_binario.seek(self.start)
            archivo_binario.write(particion.get_bytes())
            return {"status": True, "mensaje": "--Particion logica creada--\n"}
        else:
            tamano_particion = self.start + self.s
            if self.fit == "F":
                return estructura_ebr.crear_particion_siguiente_ff(archivo_binario, particion, tamano_particion)
            elif self.fit == "B":
                return estructura_ebr.crear_particion_siguiente_bf(archivo_binario, particion, tamano_particion, tamano_particion, estructura_ebr)
            elif self.fit == "W":
                return estructura_ebr.crear_particion_siguiente_wf(archivo_binario, particion, tamano_particion, 0, estructura_ebr)
            return {"status": False, "mensaje": "Error: Fit inesperado particion logica\n"}
    
    def buscar_particion_logica(self, name: str, archivo_binario):
        if self.tipo != "E":
            return None
        estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
        archivo_binario.seek(self.start)
        estructura_ebr.set_bytes(archivo_binario)
        return estructura_ebr.buscar_particion(name, archivo_binario)
    
    def eliminar_particion_logica(self, name:str, archivo_binario):
        if self.tipo != "E":
            return False
        estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
        archivo_binario.seek(self.start)
        estructura_ebr.set_bytes(archivo_binario)
        if estructura_ebr.status:
            if estructura_ebr.name == name:
                estructura_ebr.status = False
                # cambio el inicial
                archivo_binario.seek(self.start)
                archivo_binario.write(estructura_ebr.get_bytes())
                return True
        return estructura_ebr.eliminar_particion(name, archivo_binario)
    
    def add_particion_logica(self, name: str, archivo_binario, add: str):
        if self.tipo != "E":
            return False
        estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
        archivo_binario.seek(self.start)
        estructura_ebr.set_bytes(archivo_binario)
        return estructura_ebr.add_particion(name, archivo_binario, add, self.s)
    
    def reporte_particion(self, archivo_binario) -> str:
        reporte = '''
            <tr>
            <td bgcolor="/rdylgn11/3:/rdylgn11/3"><b>Particion</b></td>
            <td bgcolor="/rdylgn11/3:/rdylgn11/3"><b> </b></td>
            </tr>
            <tr>
            <td>part_status</td><td>{}</td>
            </tr>
            <tr>
            <td>part_type</td><td>{}</td>
            </tr>
            <tr>
            <td>part_fit</td><td>{}</td>
            </tr>
            <tr>
            <td>part_start</td><td>{}</td>
            </tr>
            <tr>
            <td>part_size</td><td>{}</td>
            </tr>
            <tr>
            <td>part_name</td><td>{}</td>
            </tr>'''.format(self.status, self.tipo, self.fit, self.start, self.s, self.name.replace("\0", ""))
        if self.tipo == "E":
            estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
            archivo_binario.seek(self.start)
            estructura_ebr.set_bytes(archivo_binario)
            reporte += estructura_ebr.reporte_logica(archivo_binario)
        return reporte
    
    def reporte_disk(self, archivo_binario, size_archivo: int):
        reporte = '''
            <tr>
                <td bgcolor="/rdylgn11/5:/rdylgn11/5">EBR</td>
            '''
        estructura_ebr = Ebr(False, "W", self.start, 0, -1, "")
        archivo_binario.seek(self.start)
        estructura_ebr.set_bytes(archivo_binario)
        resultado = estructura_ebr.reporte_logica_disk(archivo_binario, size_archivo, self.s) 
        fila_extendida = '<td bgcolor="/rdylgn11/3:/rdylgn11/3" COLSPAN="{}"><b>Extendida</b></td>'.format(str(resultado["conteo"]))
        reporte += resultado["result"]
        reporte += "</tr>"
        return {"extendida": reporte, "fila" : fila_extendida}