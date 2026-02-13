from ytmusicapi import YTMusic
import json
import os

def crear_playlist_yt_music(archivo_json, nombre_playlist, descripcion=""):
    """
    Crea una playlist en YouTube Music desde un archivo JSON
    
    Args:
        archivo_json: Ruta al archivo JSON con las canciones
        nombre_playlist: Nombre de la playlist a crear
        descripcion: Descripción de la playlist (opcional)
    
    Returns:
        dict: {
            'status': 'success' o 'error',
            'playlist_id': ID de la playlist creada,
            'total_canciones': Total de canciones encontradas,
            'mensaje': Mensaje descriptivo,
            'canciones_no_encontradas': Lista de canciones que no se encontraron
        }
    """
    try:
        oauth_path = 'oauth.json'
        if not os.path.exists(oauth_path):
            return {
                'status': 'error',
                'mensaje': 'No se encontró el archivo oauth.json. Ejecuta la autenticación primero.'
            }
        
        print("🔐 Autenticando con YouTube Music...")
        yt = YTMusic(oauth_path)
        
        print(f"📝 Creando playlist '{nombre_playlist}'...")
        playlist_id = yt.create_playlist(nombre_playlist, descripcion)
        print(f"✅ Playlist creada con ID: {playlist_id}")
        
        if not os.path.exists(archivo_json):
            return {'status': 'error', 'mensaje': f'No se encontró el archivo {archivo_json}'}
        
        with open(archivo_json, 'r', encoding='utf-8') as f:
            canciones = json.load(f)
        
        print(f"📋 Buscando {len(canciones)} canciones en YouTube Music...")
        
        video_ids = []
        canciones_no_encontradas = []
        
        for i, cancion in enumerate(canciones, 1):
            titulo = cancion.get('titulo') or cancion.get('name') or ''
            artista = cancion.get('artista') or cancion.get('artist') or ''
            
            if not titulo: continue
            
            query = f"{titulo} {artista}".strip()
            print(f"🔍 {i}/{len(canciones)}: Buscando '{query}'...")
            
            try:
                resultados = yt.search(query, filter="songs", limit=1)
                if resultados and len(resultados) > 0:
                    video_ids.append(resultados[0]['videoId'])
                    print(f"   ✅ Encontrada")
                else:
                    canciones_no_encontradas.append({'titulo': titulo, 'artista': artista})
                    print(f"   ❌ No encontrada")
            except Exception:
                canciones_no_encontradas.append({'titulo': titulo, 'artista': artista})
        
        if video_ids:
            print(f"\n➕ Añadiendo {len(video_ids)} canciones...")
            yt.add_playlist_items(playlist_id, video_ids)
            print(f"🎉 ¡Éxito!")
        
        return {'status': 'success', 'playlist_id': playlist_id}
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'status': 'error', 'mensaje': str(e)}

def autenticar_youtube_music():
    """
    Genera el archivo oauth.json usando el flujo simplificado.
    """
    print("=" * 60)
    print("INICIANDO AUTENTICACIÓN (MODO SIMPLIFICADO)")
    print("=" * 60)
    
    try:
        # En versiones recientes, si no pasas nada, intenta el flujo por defecto de la librería.
        # Si esto falla, te daré la alternativa de usar setup() manual.
        print("Copiando configuración de sesión...")
        setup_oauth(filepath='oauth.json')
        
        if os.path.exists('oauth.json'):
            print("\n✅ ¡Archivo 'oauth.json' generado correctamente!")
            return True
    except Exception as e:
        print(f"\n❌ Error en setup_oauth: {e}")
        print("\n💡 INTENTA ESTA ALTERNATIVA:")
        print("Si el error de 'client_id' persiste, ejecuta este comando en tu terminal:")
        print("ytmusicapi setup")
        print("(Esto te guiará para pegar los headers manualmente)")
        return False

def probar_conexion():
    """
    Verifica si el archivo funciona.
    """
    if not os.path.exists('oauth.json'): return
    try:
        yt = YTMusic("oauth.json")
        yt.get_library_playlists(limit=1)
        print("✅ Conexión validada.")
    except Exception as e:
        print(f"❌ Error de validación: {e}")

if __name__ == "__main__":
    nombre_archivo = os.path.basename(__file__)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'auth':
        if autenticar_youtube_music():
            probar_conexion()
    else:
        print(f"\nUso: python {nombre_archivo} auth")
        if os.path.exists('oauth.json'):
            probar_conexion()