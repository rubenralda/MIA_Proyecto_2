from interprete import parse, errores
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

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

if __name__ == '__main__':
    app.run(debug=True, port=4000)