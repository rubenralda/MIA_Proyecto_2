from .comando_base import Comando
import os

class Execute(Comando):

    def __init__(self, parametros: dict, lexer, parser) -> None:
        self.parametros = parametros
        self.lexer = lexer
        self.parser = parser

    def ejecutar(self):
        self.lexer.lineno = 1
        direccion = self.parametros.get("path")
        if direccion == None:
            print('--Error: Faltan parametros--')
            return False
        if not os.path.isfile(direccion):
            print("--Error: La ruta no es un archivo valido--")
            return False
        with open(direccion, "r") as comandos:
            for linea in comandos.readlines():
                resultado = self.parser.parse(linea)
                if resultado != None:
                    print('Comando a ejecutar -> ', linea.replace("\n", ""))
                    resultado.ejecutar()
            #return comandos.readlines()