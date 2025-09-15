from flask import request, Flask, jsonify, render_template
import os
from functions import llm, bbdd

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods = ['GET'])
def main():
    return render_template("index.html")

@app.route("/tutor", methods = ['POST'])
def tutor():
    data = request.get_json()

    pregunta  = data.get("pregunta")
    respuesta = llm(pregunta)

    respuesta_bbdd = bbdd(pregunta, respuesta)

    if respuesta_bbdd == "ok":
        return jsonify({"pregunta":pregunta, "respuesta": respuesta})
    else:
        return jsonify({"error": "Error al preguntar"})
    
app.run()
