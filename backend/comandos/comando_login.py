from .estructuras.estructura_superbloque import SuperBloque
from .usuario import iniciar_sesion
from .mount import obtener_particiones
from .comando_base import Comando

class Login(Comando):

    def __init__(self, parametros: dict) -> None:
        self.parametros = parametros

    def ejecutar(self):
        id = self.parametros.get("id")
        user = self.parametros.get("user")
        contra = self.parametros.get("pass")
        if id == None or user == None or contra == None:
            print("--Error: Faltan parametros--")
            return False
        particiones_montadas = obtener_particiones()
        for particion in particiones_montadas:
            if particion.id == id:
                with open(particion.path_disco, "rb+") as archivo_binario:
                    archivo_binario.seek(particion.start)
                    superbloque = SuperBloque(0,0,0)
                    superbloque.set_bytes(archivo_binario)
                    usuarios = superbloque.archivo_userstxt(archivo_binario)
                    #print(usuarios)
                    if usuarios == None:
                        print("--Error: error muy inesperado--")
                    lineas = usuarios.split("\n")[:-1]
                    lineas_grupo = lineas
                    for linea in lineas:
                        items = linea.split(",")
                        if items[1] == "G" or items[0] == "0": #es grupo o ya fue borrado
                            continue 
                        if items[3].replace(" ", "") == user:
                            if items[4].replace(" ", "") == str(contra):
                                # buscar el id grupo
                                id_grupo = ""
                                for linea_grupo in lineas_grupo:
                                    dato = linea_grupo.split(",")
                                    if dato[1] == "U" or dato[0] == "0":
                                        continue
                                    if dato[2] == items[2]:
                                        id_grupo = dato[0]
                                if iniciar_sesion(items[0], user, items[2], id, id_grupo):
                                    print("\n--Sesion iniciada--\n")
                                    return True
                                else:
                                    print("--Error: Ya hay un sesion abierta--")
                                    return False
                            else:
                                print("--Error: el password no coincide--")
                                return False
        print("--Error: Particion no encontrada--")
        return False