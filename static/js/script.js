// LEER: Trae los datos de Python y rellena los inputs
async function cargarDatos() {
    const res = await fetch('/obtener-datos');
    const datos = await res.json();

    document.getElementById('nombre').value = datos.nombre;
    document.getElementById('version').value = datos.version;
}

// MODIFICAR: Toma los valores de los inputs y los envía a Python
async function guardarCambios() {
    const status = document.getElementById('status');
    const nuevosDatos = {
        nombre: document.getElementById('nombre').value,
        version: parseFloat(document.getElementById('version').value),
        estado: "activo" // Podemos mantener valores fijos
    };

    const res = await fetch('/set-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nuevosDatos)
    });

    const data = await res.json();
    status.innerText = data.mensaje;

    // Limpiar mensaje después de 3 segundos
    setTimeout(() => status.innerText = "", 3000);
}

async function verCambios() {
    const res = await fetch('/get-config');
}