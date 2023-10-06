from .estructura_base import EstructuraBase

class Ebr(EstructuraBase):

    def __init__(self, part_status: bool, part_fit: str, part_start: int, part_s: int, part_next:int, part_name:str) -> None:
        self.status = part_status # 1 byte True si esta activo
        self.fit = part_fit # 1 byte
        self.start = part_start # 4 byte empieza a contar desde el 0
        self.size = part_s # 4 byte
        self.siguiente = part_next # 4 byte con signo
        largo_nombre = len(part_name)
        while(largo_nombre < 16):
            part_name += "\0"
            largo_nombre += 1
        self.name = part_name # 16 bytes

    def set_bytes(self, archivo_binario):
        bytes = archivo_binario.read(30)
        self.status = bool(int.from_bytes(bytes[0:1], byteorder='big'))
        self.fit = bytes[1:2].decode('utf-8')
        self.start = int.from_bytes(bytes[2:6], byteorder = 'big')
        self.size = int.from_bytes(bytes[6:10], byteorder = 'big')
        self.siguiente = int.from_bytes(bytes[10:14], byteorder = 'big', signed = True)
        self.name = bytes[14:30].decode('utf-8')

    def crear_particion_siguiente_bf(self, archivo_binario, particion, final: int, tamano_menor: int, particion_anterior):
        if self.siguiente == -1:
            if final < self.start + self.size + particion.size:
               print("--Error: la particion logica es muy grande--")
               return
            particion.start = particion_anterior.start + particion_anterior.size # va iniciar despues de actual
            particion.siguiente = particion_anterior.siguiente
            particion_anterior.siguiente = particion.start
            # cambio el siguiente
            archivo_binario.seek(particion_anterior.start)
            archivo_binario.write(particion_anterior.get_bytes())
            # escribo la nueva particion
            archivo_binario.seek(particion.start)
            archivo_binario.write(particion.get_bytes())
            print("\n--Particion logica creada--\n")
            return
        else:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            if ebr_siguiente.start - (self.start + self.size) > particion.size:
                tamano = ebr_siguiente.start - (self.start + self.size)
                if tamano < tamano_menor:
                    tamano_menor = tamano
                    particion_anterior = self
            elif tamano_menor == final:
                particion_anterior = ebr_siguiente
            ebr_siguiente.crear_particion_siguiente_bf(archivo_binario, particion, final, tamano_menor, particion_anterior)

    def crear_particion_siguiente_wf(self, archivo_binario, particion, final: int, tamano_mayor: int, particion_anterior):
        if self.siguiente == -1:
            if final < self.start + self.size + particion.size:
               print("--Error: la particion logica es muy grande--")
               return
            particion.start = particion_anterior.start + particion_anterior.size # va iniciar despues de actual
            particion.siguiente = particion_anterior.siguiente
            particion_anterior.siguiente = particion.start
            # cambio el siguiente
            archivo_binario.seek(particion_anterior.start)
            archivo_binario.write(particion_anterior.get_bytes())
            # escribo la nueva particion
            archivo_binario.seek(particion.start)
            archivo_binario.write(particion.get_bytes())
            print("\n--Particion logica creada--\n")
            return
        else:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            if ebr_siguiente.start - (self.start + self.size) > particion.size:
                tamano = ebr_siguiente.start - (self.start + self.size)
                if tamano > tamano_mayor:
                    tamano_mayor = tamano
                    particion_anterior = self
            elif tamano_mayor == 0:
                particion_anterior = ebr_siguiente
            ebr_siguiente.crear_particion_siguiente_wf(archivo_binario, particion, final, tamano_mayor, particion_anterior)

    def crear_particion_siguiente_ff(self, archivo_binario, particion, final: int):
        if self.siguiente == -1:
            if final < self.start + self.size + particion.size:
               print("--Error: la particion logica es muy grande--")
               return
            self.escribir_siguiente(archivo_binario, particion)
            print("\n--Particion logica creada--\n")
            return
        else:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            if ebr_siguiente.start - self.start + self.size < particion.size:
                self.escribir_siguiente(archivo_binario, particion)
                print("\n--Particion logica creada--\n")
                return
            ebr_siguiente.crear_particion_siguiente_ff(archivo_binario, particion, final)
        
    # escribir el siguiente ebr    
    def escribir_siguiente(self, archivo_binario, particion):
        particion.start = self.start + self.size # va iniciar despues de actual
        particion.siguiente = self.siguiente
        self.siguiente = particion.start
        # cambio el siguiente
        archivo_binario.seek(self.start)
        archivo_binario.write(self.get_bytes())
        # escribo la nueva particion
        archivo_binario.seek(particion.start)
        archivo_binario.write(particion.get_bytes())

    def buscar_particion(self, name:str, archivo_binario):
        if self.status:
            if self.name == name:
                return self
        if self.siguiente == -1:
            return None
        else:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            return ebr_siguiente.buscar_particion(name, archivo_binario)
    
    def eliminar_particion(self, name:str, archivo_binario):
        if self.siguiente == -1:
            return False
        else:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            if ebr_siguiente.name == name:
                self.siguiente = ebr_siguiente.siguiente
                # cambio el siguiente
                archivo_binario.seek(self.start)
                archivo_binario.write(self.get_bytes())
                # escribo la nueva particion
                archivo_binario.seek(ebr_siguiente.start)
                archivo_binario.write(b'\x00'*ebr_siguiente.size)
                return True
            else:
                return ebr_siguiente.eliminar_particion(name, archivo_binario)
            
    def add_particion(self, name:str, archivo_binario, add:int, final: int):
        if self.status:
            if self.name == name:
                nuevo_size = self.size + add
                if nuevo_size < 0:
                    return False
                elif self.siguiente == -1:
                    if nuevo_size > final:
                        return False
                else:
                    archivo_binario.seek(self.siguiente)
                    ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
                    ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
                    if nuevo_size >= ebr_siguiente.start:
                        return False
                self.size = nuevo_size
                archivo_binario.seek(self.start)
                archivo_binario.write(self.get_bytes())
                return True
        if self.siguiente == -1:
            return False
        else:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            return ebr_siguiente.add_particion(name, archivo_binario, add, final)
       
    def reporte_logica(self, archivo_binario) -> str:
        reporte = ""
        if self.status:
            reporte += '''
                <tr>
                <td bgcolor="/rdylgn11/5:/rdylgn11/5"><b>Particion Logica</b></td>
                <td bgcolor="/rdylgn11/5:/rdylgn11/5"><b> </b></td>
                </tr>
                <tr>
                <td>part_status</td><td>{}</td>
                </tr>
                <tr>
                <td>part_next</td><td>{}</td>
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
                </tr>'''.format(self.status, self.siguiente, self.fit, self.start, self.size, self.name.replace("\0", ""))
        if self.siguiente != -1:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            reporte += ebr_siguiente.reporte_logica(archivo_binario)
        return reporte
    
    def reporte_logica_disk(self, archivo_binario, size_archivo: int, size_particion : int):
        reporte = ""
        conteo = 1
        if not self.status:
            porcentaje = size_particion / size_archivo
            reporte += '<td>Libre5<BR/>{}%</td>'.format(str(porcentaje*100))
            conteo += 1
        else:
            porcentaje = self.size / size_archivo
            reporte += '<td>Logica<BR/>{}%</td>'.format(str(porcentaje*100))
            conteo += 1
        size_particion -= self.size
        if self.siguiente != -1:
            archivo_binario.seek(self.siguiente)
            ebr_siguiente = Ebr(False, "W", 0, 0, -1, "")
            ebr_siguiente.set_bytes(archivo_binario) # obtengo el ebr siguiente
            resultado = ebr_siguiente.reporte_logica_disk(archivo_binario, size_archivo, size_particion)
            reporte += '<td bgcolor="/rdylgn11/5:/rdylgn11/5">EBR</td>'
            reporte += resultado["result"]
            return {"conteo": resultado["conteo"] + 2, "result": reporte}
        else:
            porcentaje = size_particion / size_archivo
            if porcentaje != 0:
                reporte += '<td>Libre<BR/>{}%</td>'.format(str(porcentaje*100))
                conteo += 1
            return {"conteo": conteo, "result": reporte}