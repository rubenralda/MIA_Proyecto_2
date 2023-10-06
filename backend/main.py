from interprete import parse

while True:
    comando = input("Ingresa el comando: ")
    if (comando == "salir"):
        break
    resultado = parse(comando)
    if resultado == None:
        print("Error a leer el comando")
        continue
    resul = resultado.ejecutar() #polimorfismo donde todos los objetos heredan el metodo ejecutar