class Usuario:

    def __init__(self, id_user:int, nombre_user:str, nombre_grupo:str, id_particion:str, id_grupo:str) -> None:
        self.id_user = id_user
        self.id_grupo = id_grupo
        self.nombre_user = nombre_user
        self.nombre_grupo = nombre_grupo
        self.id_particion = id_particion
        #self.tipo = tipo # grupo o usuario
        #self.permiso = 777

usuario: Usuario = None

def iniciar_sesion(id_user:int, nombre_user:str, nombre_grupo:str, id_particion:str, id_grupo:str):
    global usuario
    if usuario == None:
        usuario = Usuario(id_user, nombre_user, nombre_grupo, id_particion, id_grupo)
        return True
    else:
        return False
    
def cerrar_sesion():
    global usuario
    if usuario == None:
        return False
    else:
        usuario = None
        return True

def is_sesion():
    global usuario
    if usuario == None:
        return False
    else:
        return True
    
def valor_usuario():
    global usuario
    return usuario