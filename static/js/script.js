// Funciones generales para la aplicación

async function cargarConfiguracion() {
    try {
        const res = await fetch('/obtener-datos');
        const datos = await res.json();
        return datos;
    } catch (err) {
        console.log("No hay configuración previa:", err);
        return null;
    }
}

async function guardarConfiguracion(config) {
    const status = document.getElementById('status');
    
    try {
        const res = await fetch('/modificar-datos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await res.json();
        
        if (status) {
            status.className = 'status success';
            status.innerText = "✅ Configuración guardada.";
            setTimeout(() => status.innerText = "", 3000);
        }
        
        return data;
    } catch (err) {
        if (status) {
            status.className = 'status error';
            status.innerText = "❌ Error al guardar configuración.";
        }
        console.error(err);
        return null;
    }
}

async function seleccionarPlataforma(plataforma, tipo = 'origen') {
    const status = document.getElementById('status');
    
    try {
        const endpoint = tipo === 'origen' ? '/guardar-origen' : '/guardar-destino';
        
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plataforma })
        });
        
        const data = await res.json();
        
        if (status) {
            status.className = 'status success';
            status.innerText = `✅ ${plataforma} seleccionado como ${tipo}`;
        }
        
        return data;
    } catch (err) {
        if (status) {
            status.className = 'status error';
            status.innerText = `❌ Error al seleccionar ${tipo}.`;
        }
        console.error(err);
        return null;
    }
}

async function iniciarScraper() {
    const status = document.getElementById('status');
    
    if (status) {
        status.className = 'status loading';
        status.innerText = "⏳ Extrayendo información... por favor espera.";
    }
    
    try {
        const res = await fetch('/iniciar-scraper', { method: 'POST' });
        const data = await res.json();
        
        if (data.status === "success") {
            if (status) {
                status.className = 'status success';
                status.innerText = `🚀 ¡Hecho! ${data.total} canciones guardadas en playlist_final.json`;
            }
            return data;
        } else {
            if (status) {
                status.className = 'status error';
                status.innerText = "❌ Error: " + data.mensaje;
            }
            return null;
        }
    } catch (err) {
        if (status) {
            status.className = 'status error';
            status.innerText = "❌ Error al conectar con el servidor.";
        }
        console.error(err);
        return null;
    }
}

// Función para validar URLs
function validarURL(url, plataforma) {
    if (!url || url.trim() === '') {
        return { valido: false, mensaje: 'Por favor ingresa una URL' };
    }
    
    const urlLower = url.toLowerCase();
    
    if (plataforma.toLowerCase() === 'spotify') {
        if (!urlLower.includes('spotify.com')) {
            return { valido: false, mensaje: 'La URL debe ser de Spotify' };
        }
    } else if (plataforma.toLowerCase() === 'ytmusic') {
        if (!urlLower.includes('music.youtube.com')) {
            return { valido: false, mensaje: 'La URL debe ser de YouTube Music' };
        }
    }
    
    return { valido: true };
}

// Función para mostrar mensajes de estado
function mostrarEstado(tipo, mensaje) {
    const status = document.getElementById('status');
    if (status) {
        status.className = `status ${tipo}`;
        status.textContent = mensaje;
        status.style.display = 'block';
    }
}

// Función para ocultar mensajes de estado
function ocultarEstado() {
    const status = document.getElementById('status');
    if (status) {
        status.style.display = 'none';
    }
}

// Exportar funciones para uso en otros scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        cargarConfiguracion,
        guardarConfiguracion,
        seleccionarPlataforma,
        iniciarScraper,
        validarURL,
        mostrarEstado,
        ocultarEstado
    };
}