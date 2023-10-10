from interprete import parse, errores
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from comandos.reportes import reportes
from comandos.usuario import *

app = Flask(__name__)

CORS(app)

@cross_origin
@app.route('/ejecutar', methods=['POST'])
def ejecutar_comando():
    respuesta = {"mensaje" : ""}
    datos = request.json
    print(datos["comando"])
    resultado = parse(datos["comando"])
    hay_error = errores()
    if hay_error != "":
        respuesta["mensaje"] = hay_error
    elif resultado == None:
        respuesta["mensaje"] = "Error: no se pudo leer el comando\n"
    else:
        respuesta["mensaje"] = resultado.ejecutar()
    print(respuesta["mensaje"])
    return jsonify(respuesta)

@cross_origin
@app.route('/reportes', methods=['GET'])
def retorno_reportes():
    direcciones = reportes()
    respuesta = {"listado" : direcciones}
    return jsonify(respuesta)

@cross_origin
@app.route('/login', methods=['GET'])
def ver_sesion():
    respuesta = {"usuario" : None, "idParticion" : None, "idUsuario" : 0}
    if is_sesion():
        respuesta["usuario"] = valor_usuario().nombre_user
        respuesta["idParticion"] = valor_usuario().id_particion
        respuesta["idUsuario"] = valor_usuario().id_user
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True, port=4000)