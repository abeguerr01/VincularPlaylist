import os
import json
import threading
import webview
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'data', 'config.json')
DATA_FILE = os.path.join(BASE_DIR, 'data', 'data.json')
RESULTS_FILE = os.path.join(BASE_DIR, 'data', 'playlist_final.json')

# Asegurar que la carpeta data existe
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

# Inicializar archivos si no existen
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "origen": "",
            "destino": "",
            "url_origen": "",
            "estado": "pendiente"
        }, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seleccionar-origen')
def seleccionar_origen():
    return render_template('seleccionar-origen.html')

@app.route('/seleccionar-destino')
def seleccionar_destino():
    return render_template('seleccionar-destino.html')

@app.route('/configurar')
def configurar():
    return render_template('configurar.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

@app.route('/obtener-datos', methods=['GET'])
def obtener_datos():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
    except Exception as e:
        print(f"Error al leer config: {e}")
    
    return jsonify({
        "origen": "",
        "destino": "",
        "url_origen": "",
        "estado": "pendiente"
    })

@app.route('/guardar-origen', methods=['POST'])
def guardar_origen():
    try:
        data = request.json
        plataforma = data.get('plataforma')
        
        print(f"Guardando origen: {plataforma}")
        
        # Leer config existente o crear nueva
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config['origen'] = plataforma
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"Origen guardado exitosamente: {plataforma}")
        return jsonify({"status": "success", "origen": plataforma})
    
    except Exception as e:
        print(f"Error en guardar-origen: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "mensaje": str(e)}), 500

@app.route('/guardar-destino', methods=['POST'])
def guardar_destino():
    try:
        data = request.json
        plataforma = data.get('plataforma')
        
        print(f"Guardando destino: {plataforma}")
        
        # Leer config existente
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config['destino'] = plataforma
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"Destino guardado exitosamente: {plataforma}")
        return jsonify({"status": "success", "destino": plataforma})
    
    except Exception as e:
        print(f"Error en guardar-destino: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "mensaje": str(e)}), 500

@app.route('/guardar-url', methods=['POST'])
def guardar_url():
    try:
        data = request.json
        url = data.get('url')
        
        print(f"Guardando URL: {url}")
        
        # Leer config existente
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config['url_origen'] = url
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print("URL guardada exitosamente")
        return jsonify({"status": "success"})
    
    except Exception as e:
        print(f"Error en guardar-url: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "mensaje": str(e)}), 500

@app.route('/iniciar-migracion', methods=['POST'])
def iniciar_migracion():
    try:
        print("Iniciando migración...")
        
        # Leer configuración
        if not os.path.exists(CONFIG_FILE):
            return jsonify({"status": "error", "mensaje": "No hay configuración"}), 400
        
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        url = config.get('url_origen')
        origen = config.get('origen', '').lower()
        destino = config.get('destino')

        print(f"Config: origen={origen}, destino={destino}, url={url}")

        if not url or not origen:
            return jsonify({"status": "error", "mensaje": "Faltan datos de configuración"}), 400

        # Importar scrapers
        try:
            import scripts.exportScraper as exportScraper
            print("Módulo exportScraper importado correctamente")
        except ImportError as e:
            print(f"Error al importar exportScraper: {e}")
            return jsonify({
                "status": "error",
                "mensaje": f"No se pudo importar el módulo de scraping: {str(e)}"
            }), 500

        # Ejecutar el scraper correspondiente
        canciones = []
        
        if origen == "spotify":
            print("Ejecutando scraper de Spotify...")
            try:
                canciones = exportScraper.scrape_spotify_playlist(url, RESULTS_FILE)
                print(f"Scraper completado: {len(canciones)} canciones")
            except AttributeError:
                return jsonify({
                    "status": "error",
                    "mensaje": "La función scrape_spotify_playlist no existe en exportScraper.py"
                }), 500
                
        elif origen == "ytmusic":
            print("Ejecutando scraper de YouTube Music...")
            try:
                canciones = exportScraper.scrape_yt_music_playlist(url, RESULTS_FILE)
                print(f"Scraper completado: {len(canciones)} canciones")
            except AttributeError:
                return jsonify({
                    "status": "error",
                    "mensaje": "La función scrape_yt_music_playlist no existe en exportScraper.py"
                }), 500
        else:
            return jsonify({"status": "error", "mensaje": f"Plataforma de origen no válida: {origen}"}), 400
        
        # Actualizar config con el resultado
        config['estado'] = 'completado'
        config['total_canciones'] = len(canciones)
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print("Migración completada exitosamente")
        
        return jsonify({
            "status": "success", 
            "total": len(canciones),
            "origen": origen,
            "destino": destino,
            "mensaje": f"Extraídas {len(canciones)} canciones de {origen}"
        })
        
    except Exception as e:
        print(f"Error en iniciar-migracion: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "mensaje": f"Error al extraer playlist: {str(e)}"
        }), 500

@app.route('/obtener-resultados', methods=['GET'])
def obtener_resultados():
    try:
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                canciones = json.load(f)
            
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            return jsonify({
                "status": "success",
                "canciones": canciones,
                "config": config
            })
        return jsonify({"status": "error", "mensaje": "No hay resultados"}), 404
    
    except Exception as e:
        print(f"Error en obtener-resultados: {e}")
        return jsonify({"status": "error", "mensaje": str(e)}), 500

@app.route('/importar-ytmusic', methods=['POST'])
def importar_yt_music():
    try:
        print("📤 Iniciando importación a YouTube Music...")
        
        # Verificar que existe el archivo de resultados
        if not os.path.exists(RESULTS_FILE):
            return jsonify({
                "status": "error",
                "mensaje": "No hay canciones para importar. Primero extrae una playlist."
            }), 400
        
        # Obtener datos de la configuración
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        # Importar el módulo de importación - MÚLTIPLES INTENTOS
        crear_playlist_yt_music = None
        
        # Intento 1: Import normal
        try:
            from scripts.importYTmusic import crear_playlist_yt_music
            print("✅ Módulo importado (método 1)")
        except ImportError:
            pass
        
        # Intento 2: Import con sys.path
        if crear_playlist_yt_music is None:
            try:
                import sys
                scripts_path = os.path.join(BASE_DIR, 'scripts')
                if scripts_path not in sys.path:
                    sys.path.insert(0, scripts_path)
                from importYTmusic import crear_playlist_yt_music
                print("✅ Módulo importado (método 2)")
            except ImportError:
                pass
        
        # Intento 3: Import absoluto
        if crear_playlist_yt_music is None:
            try:
                import importlib.util
                module_path = os.path.join(BASE_DIR, 'scripts', 'importYTmusic.py')
                spec = importlib.util.spec_from_file_location("importYTmusic", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                crear_playlist_yt_music = module.crear_playlist_yt_music
                print("✅ Módulo importado (método 3)")
            except Exception as e:
                print(f"❌ Error en método 3: {e}")
        
        # Si ningún método funcionó
        if crear_playlist_yt_music is None:
            print("❌ No se pudo importar el módulo")
            return jsonify({
                "status": "error",
                "mensaje": "No se pudo importar el módulo importYTmusic. Verifica que existe scripts/importYTmusic.py"
            }), 500
        
        # Obtener datos del request (nombre y descripción de la playlist)
        data = request.json or {}
        nombre_playlist = data.get('nombre_playlist', 'Playlist Migrada')
        descripcion = data.get('descripcion', f'Migración desde {config.get("origen", "otra plataforma")}')
        
        print(f"📝 Creando playlist: {nombre_playlist}")
        print(f"📄 Descripción: {descripcion}")
        
        # Ejecutar la importación
        resultado = crear_playlist_yt_music(RESULTS_FILE, nombre_playlist, descripcion)
        
        if resultado['status'] == 'success':
            print(f"✅ Importación exitosa: {resultado['mensaje']}")
            
            # Actualizar configuración con el resultado
            config['importacion_ytmusic'] = {
                'playlist_id': resultado['playlist_id'],
                'total_importadas': resultado['total_canciones'],
                'fecha': json.dumps({"timestamp": "now"})  # Podrías usar datetime aquí
            }
            
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            return jsonify(resultado)
        else:
            print(f"❌ Error en importación: {resultado['mensaje']}")
            return jsonify(resultado), 500
    
    except Exception as e:
        print(f"❌ Error en importar-ytmusic: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "mensaje": f"Error al importar a YouTube Music: {str(e)}"
        }), 500

@app.route('/autenticar-ytmusic', methods=['POST'])
def autenticar_ytmusic():
    """
    Inicia el proceso de autenticación con YouTube Music
    NOTA: Esta ruta debe usarse con precaución ya que requiere interacción del usuario
    """
    try:
        print("🔐 Iniciando autenticación con YouTube Music...")
        
        # Importar con múltiples métodos
        autenticar_youtube_music = None
        
        # Intento 1: Import normal
        try:
            from scripts.importYTmusic import autenticar_youtube_music
            print("✅ Función de autenticación importada (método 1)")
        except ImportError:
            pass
        
        # Intento 2: Import con sys.path
        if autenticar_youtube_music is None:
            try:
                import sys
                scripts_path = os.path.join(BASE_DIR, 'scripts')
                if scripts_path not in sys.path:
                    sys.path.insert(0, scripts_path)
                from importYTmusic import autenticar_youtube_music
                print("✅ Función de autenticación importada (método 2)")
            except ImportError:
                pass
        
        # Intento 3: Import absoluto
        if autenticar_youtube_music is None:
            try:
                import importlib.util
                module_path = os.path.join(BASE_DIR, 'scripts', 'importYTmusic.py')
                spec = importlib.util.spec_from_file_location("importYTmusic", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                autenticar_youtube_music = module.autenticar_youtube_music
                print("✅ Función de autenticación importada (método 3)")
            except Exception as e:
                print(f"❌ Error en método 3: {e}")
        
        if autenticar_youtube_music is None:
            return jsonify({
                "status": "error",
                "mensaje": "No se pudo importar la función de autenticación"
            }), 500
        
        resultado = autenticar_youtube_music()
        
        return jsonify(resultado)
    
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return jsonify({
            "status": "error",
            "mensaje": f"Error en autenticación: {str(e)}"
        }), 500

def run_flask():
    print("Iniciando servidor Flask en http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    print("=" * 50)
    print("Iniciando aplicación de Migración de Playlist")
    print("=" * 50)
    print(f"Directorio base: {BASE_DIR}")
    print(f"Archivo de configuración: {CONFIG_FILE}")
    print(f"Archivo de resultados: {RESULTS_FILE}")
    print("=" * 50)
    
    # Iniciar Flask en un hilo separado
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Esperar a que Flask inicie
    import time
    time.sleep(2)
    
    # Intentar abrir ventana con pywebview
    try:
        print("Abriendo ventana de aplicación...")
        webview.create_window('Migración de Playlist', 'http://127.0.0.1:5000', width=900, height=700)
        webview.start()
    except Exception as e:
        print(f"No se pudo crear ventana con pywebview: {e}")
        print("\n" + "=" * 50)
        print("ACCEDE A LA APLICACIÓN EN:")
        print("http://127.0.0.1:5000")
        print("=" * 50 + "\n")
        
        # Mantener el servidor corriendo
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nServidor detenido")