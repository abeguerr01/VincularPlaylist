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
        # Verificar que existe el archivo oauth.json
        oauth_path = 'oauth.json'
        if not os.path.exists(oauth_path):
            return {
                'status': 'error',
                'mensaje': 'No se encontró el archivo oauth.json. Ejecuta la autenticación primero.'
            }
        
        # Autenticar con YouTube Music
        print("🔐 Autenticando con YouTube Music...")
        yt = YTMusic(oauth_path)
        
        # Crear playlist
        print(f"📝 Creando playlist '{nombre_playlist}'...")
        playlist_id = yt.create_playlist(nombre_playlist, descripcion)
        print(f"✅ Playlist creada con ID: {playlist_id}")
        
        # Leer canciones del archivo JSON
        if not os.path.exists(archivo_json):
            return {
                'status': 'error',
                'mensaje': f'No se encontró el archivo {archivo_json}'
            }
        
        with open(archivo_json, 'r', encoding='utf-8') as f:
            canciones = json.load(f)
        
        print(f"📋 Buscando {len(canciones)} canciones en YouTube Music...")
        
        # Buscar y agregar canciones
        video_ids = []
        canciones_no_encontradas = []
        
        for i, cancion in enumerate(canciones, 1):
            titulo = cancion.get('titulo') or cancion.get('name') or ''
            artista = cancion.get('artista') or cancion.get('artist') or ''
            
            if not titulo:
                print(f"⚠️  Canción {i}/{len(canciones)}: Sin título, omitiendo...")
                continue
            
            query = f"{titulo} {artista}".strip()
            print(f"🔍 {i}/{len(canciones)}: Buscando '{query}'...")
            
            try:
                resultados = yt.search(query, filter="songs", limit=1)
                
                if resultados and len(resultados) > 0:
                    video_ids.append(resultados[0]['videoId'])
                    print(f"   ✅ Encontrada: {titulo} - {artista}")
                else:
                    canciones_no_encontradas.append({
                        'titulo': titulo,
                        'artista': artista
                    })
                    print(f"   ❌ No encontrada: {titulo} - {artista}")
            
            except Exception as e:
                print(f"   ⚠️  Error al buscar: {e}")
                canciones_no_encontradas.append({
                    'titulo': titulo,
                    'artista': artista,
                    'error': str(e)
                })
        
        # Añadir canciones a la playlist
        if video_ids:
            print(f"\n➕ Añadiendo {len(video_ids)} canciones a la playlist...")
            yt.add_playlist_items(playlist_id, video_ids)
            print(f"🎉 ¡Playlist '{nombre_playlist}' creada exitosamente!")
        else:
            print("⚠️  No se encontraron canciones para agregar")
        
        # Retornar resultado
        return {
            'status': 'success',
            'playlist_id': playlist_id,
            'total_canciones': len(video_ids),
            'total_buscadas': len(canciones),
            'mensaje': f"Playlist creada con {len(video_ids)} de {len(canciones)} canciones",
            'canciones_no_encontradas': canciones_no_encontradas
        }
    
    except Exception as e:
        print(f"❌ Error al crear playlist: {e}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'mensaje': f"Error al crear playlist: {str(e)}"
        }


def autenticar_youtube_music():
    """
    Script simple de autenticación para YouTube Music
    Ejecuta: python autenticar_ytmusic.py
    """

    print("=" * 60)
    print("AUTENTICACIÓN DE YOUTUBE MUSIC")
    print("=" * 60)
    print()

    # Intentar importar ytmusicapi
    try:
        from ytmusicapi import setup_oauth
        print("✅ ytmusicapi instalado correctamente")
    except ImportError:
        print("❌ ytmusicapi no está instalado")
        print("\nInstálalo con:")
        print("  pip install ytmusicapi")
        print()
        input("Presiona Enter para salir...")
        exit(1)

    # Mostrar instrucciones
    print("\n🔐 Iniciando autenticación...")
    print("\n📋 INSTRUCCIONES:")
    print("1. Se abrirá tu navegador automáticamente")
    print("2. Inicia sesión con tu cuenta de Google/YouTube")
    print("3. Acepta TODOS los permisos solicitados")
    print("4. Copia el código que aparece")
    print("5. Vuelve aquí y pégalo cuando se te solicite")
    print()

    input("Presiona Enter cuando estés listo para continuar...")
    print()

    # Ejecutar autenticación
    try:
        print("🌐 Abriendo navegador...")
        setup_oauth(filepath='oauth.json')
        
        print()
        print("=" * 60)
        print("✅ ¡AUTENTICACIÓN EXITOSA!")
        print("=" * 60)
        print()
        print("📁 Archivo oauth.json creado correctamente")
        print()
        print("🎉 Ya puedes usar la función de importar a YouTube Music")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Autenticación cancelada por el usuario")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR EN LA AUTENTICACIÓN")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("💡 SOLUCIONES:")
        print()
        print("1. Verifica que ytmusicapi esté actualizado:")
        print("   pip install --upgrade ytmusicapi")
        print()
        print("2. Prueba el método manual:")
        print("   Lee el archivo AUTENTICACION_MANUAL_YTMUSIC.md")
        print()
        print("3. Si el error persiste, usa el método del OAuth Playground")
        print("   (ver AUTENTICACION_MANUAL_YTMUSIC.md)")
        print()

    input("\nPresiona Enter para salir...")


# Para ejecutar la autenticación manualmente desde consola
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'auth':
        autenticar_youtube_music()
    else:
        print("Uso:")
        print("  python importYTmusic.py auth    - Para autenticar")
        print("\nO importa las funciones en tu código:")
        print("  from scripts.importYTmusic import crear_playlist_yt_music")