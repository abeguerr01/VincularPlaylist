import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import os

# Configuración (obtén tus credenciales en https://developer.spotify.com/dashboard)
CLIENT_ID = 'tu_client_id'
CLIENT_SECRET = 'tu_client_secret'

# Inicializar cliente de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def guardar_playlist_csv(playlist_url, filename):
    """Guarda una playlist de Spotify en un archivo CSV."""
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Título', 'Artista', 'Álbum'])
        for item in tracks:
            track = item['track']
            artist = track['artists'][0]['name']
            title = track['name']
            album = track['album']['name']
            writer.writerow([title, artist, album])
    print(f"✅ Playlist guardada en {filename}")

def cargar_playlist_csv(filename):
    """Carga una playlist desde un archivo CSV y devuelve una lista de diccionarios."""
    if not os.path.exists(filename):
        print("❌ El archivo no existe.")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Ejemplo de uso
URL_PLAYLIST = "https://open.spotify.com/playlist/37i9dQZF1E4v3XQRJGOY9x"
ARCHIVO_CSV = "mi_playlist.csv"

# Guardar playlist
guardar_playlist_csv(URL_PLAYLIST, ARCHIVO_CSV)

# Cargar playlist
datos = cargar_playlist_csv(ARCHIVO_CSV)
for fila in datos[:5]:  # Mostrar primeras 5 canciones
    print(fila['Título'], "–", fila['Artista'])   