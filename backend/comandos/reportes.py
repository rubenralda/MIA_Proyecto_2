direcciones_reportes = []

def agregar_reportes(direccion:str):
    global direcciones_reportes
    direcciones_reportes.append(direccion)
    
def reportes():
    global direcciones_reportes
    return direcciones_reportes