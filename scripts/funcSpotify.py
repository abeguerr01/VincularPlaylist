from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configuración de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='TU_CLIENT_ID',
    client_secret='TU_CLIENT_SECRET'
))

# Inicializar YouTube Music (requiere autenticación previa con OAuth)
ytmusic = YTMusic('oauth.json')

# Obtener playlist de Spotify
playlist_id = 'ID_DE_LA_PLAYLIST_SPOTIFY'
spotify_playlist = sp.playlist(playlist_id)

# Crear playlist en YouTube Music
playlist_title = spotify_playlist['name']
playlist_description = spotify_playlist.get('description', '')

new_playlist_id = ytmusic.create_playlist(
    title=playlist_title,
    description=playlist_description
)

# Buscar y añadir canciones
video_ids = []
for item in spotify_playlist['tracks']['items']:
    track = item['track']
    query = f"{track['name']} {track['artists'][0]['name']}"
    search_results = ytmusic.search(query, filter="songs", limit=1)
    if search_results:
        video_ids.append(search_results[0]['videoId'])

# Añadir canciones a la nueva playlist
if video_ids:
    ytmusic.add_playlist_items(new_playlist_id, video_ids)

print(f"Playlist creada en YouTube Music con ID: {new_playlist_id}")   