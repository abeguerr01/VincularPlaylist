import os
import json
import threading
import webview
from flask import Flask, render_template, request, jsonify
import scripts.scraper as scraper

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'data', 'data.json')
RESULTS_FILE = os.path.join(BASE_DIR, 'data', 'playlist_final.json')

# Asegurar que la carpeta data existe
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obtener-datos', methods=['GET'])
def obtener_datos():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({"plataforma": "ytmusic", "url": ""})

@app.route('/modificar-datos', methods=['POST'])
def modificar_datos():
    nuevos_datos = request.json
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(nuevos_datos, f, indent=4, ensure_ascii=False)
    return jsonify({"status": "success"})

@app.route('/iniciar-scraper', methods=['POST'])
def iniciar_scraper_route():
    # 1. Leer lo que el usuario guardó
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    url = config.get('url')
    plataforma = config.get('plataforma')

    if not url:
        return jsonify({"status": "error", "mensaje": "No hay URL configurada"}), 400

    # 2. Ejecutar el scraper correspondiente
    if plataforma == "spotify":
        canciones = scraper.scrape_spotify_playlist(url, RESULTS_FILE)
    else:
        canciones = scraper.scrape_yt_music_playlist(url, RESULTS_FILE)

    return jsonify({
        "status": "success", 
        "total": len(canciones),
        "mensaje": f"Extraídas {len(canciones)} canciones de {plataforma}"
    })

def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    webview.create_window('Vincular Playlist', 'http://localhost:5000')
    webview.start()