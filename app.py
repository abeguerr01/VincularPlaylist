import webview
import threading
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
JSON_FILE = 'data/config.json'

#Ruta inicial
@app.route('/')
def index():
    return render_template('index.html')


# -- Rutas de y opciones -- #

@app.route('/get-config', methods=['GET'])
def getConfig():
    with open(JSON_FILE, 'r') as f:
        datos = json.load(f)
    return jsonify(datos)

@app.route('/set-config', methods=['POST'])
def setConfig():
    nuevos_datos = request.json
    with open(JSON_FILE, 'w') as f:
        json.dump(nuevos_datos, f, indent=4) # indent=4 para que sea legible
    return jsonify({"mensaje": "¡JSON actualizado!"})

@app.route('/testing')
def testing():
    return render_template('testing.html')



#################################################
# -- Código para ejecutar la app con webview -- #
#################################################

def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    webview.create_window('Editor JSON', 'http://localhost:5000')
    webview.start()