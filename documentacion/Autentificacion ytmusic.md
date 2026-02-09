# 🔐 Guía de Autenticación de YouTube Music

Para poder importar playlists a YouTube Music, necesitas autenticarte **UNA VEZ**. Sigue estos pasos:

## 📋 Requisitos previos

1. Tener instalado `ytmusicapi`:
   ```bash
   pip install ytmusicapi
   ```

2. Tener una cuenta de Google/YouTube

## 🚀 Proceso de autenticación

### Opción 1: Desde la terminal (RECOMENDADO)

```bash
# Navega a la carpeta de tu proyecto
cd ruta/a/VINCULARPLAYLIST

# Ejecuta el script de autenticación
python scripts/importYTmusic.py auth
```

### Opción 2: Manualmente con Python

```python
from ytmusicapi import YTMusic

# Esto abrirá tu navegador
YTMusic.setup(filepath='oauth.json')
```

## 📝 Pasos del proceso

1. **Se abrirá tu navegador automáticamente**
   - Si no se abre, copia la URL que aparece en la consola

2. **Inicia sesión en Google**
   - Usa la cuenta donde quieres crear las playlists

3. **Acepta los permisos**
   - La aplicación necesita acceso a tu biblioteca de YouTube Music

4. **Copia el código**
   - Después de aceptar, verás un código
   - Copia ese código completo

5. **Pega el código en la terminal**
   - Pégalo cuando se te solicite
   - Presiona Enter

6. **¡Listo!**
   - Se creará un archivo `oauth.json` en tu proyecto
   - Este archivo contiene tu token de autenticación

## 📁 Archivo oauth.json

Una vez completado el proceso, verás un archivo `oauth.json` en la raíz de tu proyecto:

```
VINCULARPLAYLIST/
├── app.py
├── oauth.json          ← Este archivo se crea automáticamente
├── data/
├── scripts/
└── ...
```

**⚠️ IMPORTANTE:**
- NO compartas este archivo con nadie
- NO lo subas a GitHub o repositorios públicos
- Añádelo a tu `.gitignore`:
  ```
  oauth.json
  ```

## 🔄 Renovación del token

El token de `oauth.json` puede expirar después de un tiempo. Si ves errores de autenticación:

1. Elimina el archivo `oauth.json`
2. Vuelve a ejecutar el proceso de autenticación

## ❌ Solución de problemas

### Error: "oauth.json no encontrado"

**Solución:** Ejecuta el proceso de autenticación primero.

### Error: "Token expirado"

**Solución:** Elimina `oauth.json` y vuelve a autenticarte.

### Error: "No se pudo abrir el navegador"

**Solución:** 
1. Copia manualmente la URL que aparece en la consola
2. Ábrela en tu navegador
3. Sigue el proceso normalmente

### Error: "Permisos denegados"

**Solución:** 
1. Asegúrate de aceptar TODOS los permisos solicitados
2. Verifica que la cuenta tenga acceso a YouTube Music

## 🧪 Probar la autenticación

Después de autenticarte, prueba que funciona:

```python
from ytmusicapi import YTMusic

yt = YTMusic('oauth.json')
print("✅ Autenticación exitosa")

# Ver tus playlists
playlists = yt.get_library_playlists(limit=5)
for playlist in playlists:
    print(f"📝 {playlist['title']}")
```

## 📚 Uso en la aplicación

Una vez autenticado, el botón "Importar a YouTube Music" en la página de resultados funcionará automáticamente. Solo:

1. Extrae tu playlist de Spotify/YT Music
2. Ve a los resultados
3. Haz clic en "Importar a YouTube Music"
4. Ingresa el nombre de la nueva playlist
5. ¡Listo!

## 🔒 Seguridad

- El archivo `oauth.json` es personal e intransferible
- Guárdalo de forma segura
- No lo compartas por correo, chat, etc.
- Si crees que fue comprometido, elimínalo y genera uno nuevo

## 📞 Más información

Documentación oficial de ytmusicapi:
https://ytmusicapi.readthedocs.io/en/stable/setup.html