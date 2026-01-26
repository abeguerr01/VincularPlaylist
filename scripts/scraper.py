import json
import os
from playwright.sync_api import sync_playwright

def scrape_yt_music_playlist(url, ruta_json):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", 
            locale="es-ES"
        )
        page = context.new_page()
        
        print(f"Log: Navegando a YT Music: {url}")
        page.goto(url)

        # Salto de cookies
        try:
            selector_boton = 'button:has-text("Aceptar todo"), button:has-text("Acepto")'
            page.wait_for_selector(selector_boton, timeout=5000)
            page.click(selector_boton)
        except:
            pass

        page.wait_for_load_state("networkidle")
        try:
            page.wait_for_selector('ytmusic-responsive-list-item-renderer', timeout=10000)
        except:
            print("Log: No se encontraron canciones en YT Music.")
            browser.close()
            return []

        canciones = []
        filas = page.query_selector_all('ytmusic-responsive-list-item-renderer')

        for fila in filas:
            try:
                columnas = fila.query_selector_all('.flex-column')
                titulo = columnas[0].query_selector('a').inner_text()
                metadatos = columnas[1].query_selector_all('a')
                artista = metadatos[0].inner_text() if len(metadatos) > 0 else "N/A"
                album = metadatos[1].inner_text() if len(metadatos) > 1 else "N/A"
                duracion = fila.query_selector('.fixed-column').inner_text().strip()

                canciones.append({
                    "titulo": titulo,
                    "artista": artista,
                    "album": album,
                    "duracion": duracion
                })
            except:
                continue

        # --- GUARDADO EN JSON ---
        if canciones:
            os.makedirs(os.path.dirname(ruta_json), exist_ok=True)
            with open(ruta_json, 'w', encoding='utf-8') as f:
                json.dump(canciones, f, indent=4, ensure_ascii=False)
            print(f"Log: {len(canciones)} canciones guardadas en {ruta_json}")

        browser.close()
        return canciones

def scrape_spotify_playlist(url, ruta_json):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"Log: Accediendo a Spotify: {url}")
        page.goto(url)

        try:
            page.wait_for_selector('[data-testid="tracklist-row"]', timeout=15000)
        except:
            print("Log: No se pudo cargar la lista de Spotify.")
            browser.close()
            return []

        canciones = []
        filas = page.query_selector_all('[data-testid="tracklist-row"]')

        for fila in filas:
            try:
                titulo_elem = fila.query_selector('div[dir="auto"]')
                titulo = titulo_elem.inner_text() if titulo_elem else "N/A"

                enlaces = fila.query_selector_all('a[href*="/artist/"], a[href*="/album/"]')
                artistas_list = [e.inner_text() for e in enlaces if "/artist/" in e.get_attribute("href")]
                artista = ", ".join(artistas_list) if artistas_list else "N/A"
                
                album_elem = next((e for e in enlaces if "/album/" in e.get_attribute("href")), None)
                album = album_elem.inner_text() if album_elem else "N/A"

                duracion_elem = fila.query_selector('div:has-text(":")') 
                duracion = duracion_elem.inner_text() if duracion_elem else "N/A"

                canciones.append({
                    "titulo": titulo,
                    "artista": artista,
                    "album": album,
                    "duracion": duracion
                })
            except:
                continue

        # --- GUARDADO EN JSON ---
        if canciones:
            os.makedirs(os.path.dirname(ruta_json), exist_ok=True)
            with open(ruta_json, 'w', encoding='utf-8') as f:
                json.dump(canciones, f, indent=4, ensure_ascii=False)
            print(f"Log: {len(canciones)} canciones guardadas en {ruta_json}")

        browser.close()
        return canciones