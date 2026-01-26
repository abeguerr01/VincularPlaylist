async function cargarConfiguracion() {
    try {
        const res = await fetch('/obtener-datos');
        const datos = await res.json();
        if (datos.plataforma) document.getElementById('plataforma').value = datos.plataforma;
        if (datos.url) document.getElementById('url').value = datos.url;
    } catch (err) {
        console.log("No hay configuración previa.");
    }
}

async function guardarConfiguracion() {
    const status = document.getElementById('status');
    const config = {
        plataforma: document.getElementById('plataforma').value,
        url: document.getElementById('url').value
    };

    const res = await fetch('/modificar-datos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
    });

    const data = await res.json();
    status.innerText = "✅ Configuración guardada en data.json.";
    setTimeout(() => status.innerText = "", 3000);
}

async function iniciarScraper() {
    const status = document.getElementById('status');
    status.innerText = "⏳ Extrayendo información... por favor espera.";
    
    try {
        // Ahora llamamos a una única ruta que decide si es YT o Spotify
        const res = await fetch('/iniciar-scraper', { method: 'POST' });
        const data = await res.json();
        
        if (data.status === "success") {
            status.innerText = `🚀 ¡Hecho! ${data.total} canciones guardadas en playlist_final.json`;
        } else {
            status.innerText = "❌ Error: " + data.mensaje;
        }
    } catch (err) {
        status.innerText = "❌ Error al conectar con el servidor.";
    }
}