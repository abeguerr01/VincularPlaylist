# 📖 Guía Completa de Uso

## 🎯 Flujo completo: Spotify → YouTube Music

### Paso 1: Preparación inicial (Una sola vez)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Autenticar YouTube Music
python scripts/importYTmusic.py auth
```

Sigue las instrucciones en pantalla para completar la autenticación.

### Paso 2: Ejecutar la aplicación

```bash
python app.py
```

### Paso 3: Exportar playlist de Spotify

1. Ve a Spotify y abre la playlist que quieres migrar
2. Haz clic en los 3 puntos (···)
3. Compartir → Copiar enlace de la playlist
4. La URL se verá así: `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`

### Paso 4: Usar la aplicación

1. **Pantalla inicial**: Haz clic en "EMPEZAR"

2. **Seleccionar origen**: Haz clic en "🎵 Spotify"

3. **Seleccionar destino**: Haz clic en "▶️ YouTube Music"

4. **Configurar**:
   - Pega la URL de tu playlist de Spotify
   - Haz clic en "🚀 Iniciar Migración"
   - Espera a que se complete (puede tomar varios minutos)

5. **Resultados**:
   - Verás la lista de todas las canciones extraídas
   - Haz clic en "▶️ Importar a YouTube Music"
   - Ingresa el nombre para tu nueva playlist
   - ¡Listo! Tu playlist está en YouTube Music

## 🔄 Flujo completo: YouTube Music → Spotify

### Paso 1: Exportar playlist de YouTube Music

1. Abre YouTube Music
2. Ve a la playlist que quieres exportar
3. Copia la URL (se verá así: `https://music.youtube.com/playlist?list=RDCLAK5uy_k...`)

### Paso 2: Usar la aplicación

1. Selecciona "YouTube Music" como origen
2. Selecciona "Spotify" como destino
3. Pega la URL
4. Haz clic en "Iniciar Migración"

### Paso 3: Importar a Spotify

**NOTA:** Para importar a Spotify necesitarás crear un script similar al de YouTube Music usando la API de Spotify. Este script aún no está implementado.

## 📝 Ejemplos de URLs válidas

### Spotify
```
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
https://open.spotify.com/playlist/6UeSakyzhiEt4NB3UAd6NQ?si=abc123
```

### YouTube Music
```
https://music.youtube.com/playlist?list=RDCLAK5uy_kmPRjHDECIcuVwnKsx8gh_Q94Vb6ktPNg
https://music.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
```

## 🎵 Formato de datos exportados

Las canciones se guardan en `data/playlist_final.json`:

```json
[
    {
        "titulo": "Bohemian Rhapsody",
        "artista": "Queen",
        "album": "A Night at the Opera"
    },
    {
        "titulo": "Stairway to Heaven",
        "artista": "Led Zeppelin",
        "album": "Led Zeppelin IV"
    }
]
```

## ⚙️ Configuración guardada

La configuración se guarda en `data/config.json`:

```json
{
    "origen": "Spotify",
    "destino": "YTMusic",
    "url_origen": "https://open.spotify.com/playlist/...",
    "estado": "completado",
    "total_canciones": 50,
    "importacion_ytmusic": {
        "playlist_id": "PLrAXtmErZgO...",
        "total_importadas": 48,
        "fecha": "2024-02-09"
    }
}
```

## 🔧 Funciones disponibles en scripts

### scripts/exportScraper.py

```python
from scripts.exportScraper import scrape_spotify_playlist, scrape_yt_music_playlist

# Exportar de Spotify
canciones = scrape_spotify_playlist(
    url='https://open.spotify.com/playlist/...',
    output_file='data/playlist_final.json'
)

# Exportar de YouTube Music
canciones = scrape_yt_music_playlist(
    url='https://music.youtube.com/playlist?list=...',
    output_file='data/playlist_final.json'
)
```

### scripts/importYTmusic.py

```python
from scripts.importYTmusic import crear_playlist_yt_music, autenticar_youtube_music

# Autenticar (una sola vez)
autenticar_youtube_music()

# Crear playlist en YouTube Music
resultado = crear_playlist_yt_music(
    archivo_json='data/playlist_final.json',
    nombre_playlist='Mi Playlist Migrada',
    descripcion='Playlist migrada desde Spotify'
)

print(f"Playlist creada: {resultado['playlist_id']}")
print(f"Canciones añadidas: {resultado['total_canciones']}")
```

## 📊 Manejo de errores comunes

### Canciones no encontradas

Es normal que algunas canciones no se encuentren en YouTube Music. Esto puede pasar por:

- Nombre de artista o canción ligeramente diferente
- Canción no disponible en YouTube Music
- Versiones diferentes (live, remix, etc.)

El script reportará cuáles canciones no se encontraron.

### Límites de tasa

Si tienes una playlist muy grande (1000+ canciones), puede que encuentres límites de tasa de la API. En ese caso:

1. Divide la playlist en partes más pequeñas
2. Espera unos minutos entre importaciones

## 🎯 Mejores prácticas

1. **Nombres descriptivos**: Dale nombres claros a tus playlists
2. **Verifica los resultados**: Revisa la lista de canciones antes de importar
3. **Guarda los archivos JSON**: Por si necesitas reimportar
4. **Privacidad**: No compartas tu `oauth.json`

## 🚀 Casos de uso avanzados

### Migrar múltiples playlists

```bash
# 1. Exporta la primera playlist
# 2. Importa a YouTube Music
# 3. Guarda el archivo playlist_final.json con otro nombre
# 4. Repite el proceso
```

### Combinar playlists

```python
import json

# Cargar múltiples playlists
with open('playlist1.json') as f:
    p1 = json.load(f)

with open('playlist2.json') as f:
    p2 = json.load(f)

# Combinar (sin duplicados)
canciones_combinadas = p1 + p2
canciones_unicas = []
titulos_vistos = set()

for cancion in canciones_combinadas:
    titulo = cancion['titulo']
    if titulo not in titulos_vistos:
        canciones_unicas.append(cancion)
        titulos_vistos.add(titulo)

# Guardar playlist combinada
with open('playlist_combinada.json', 'w', encoding='utf-8') as f:
    json.dump(canciones_unicas, f, indent=4, ensure_ascii=False)
```

## 📞 Soporte

Si encuentras problemas:

1. Revisa `SOLUCION_PROBLEMAS.md`
2. Revisa los logs en la consola
3. Verifica que todos los archivos estén en su lugar
4. Asegúrate de estar autenticado correctamente

## 🎉 ¡Y eso es todo!

Ahora tienes todo listo para migrar tus playlists entre plataformas de forma sencilla.