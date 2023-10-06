from .comando_base import Comando

class Pausa(Comando):

    def __init__(self) -> None:
        super().__init__()
    
    def ejecutar(self):
        while True:
            tecla = input("Presiona la tecla Enter para continuar")
            if tecla == "":
                break