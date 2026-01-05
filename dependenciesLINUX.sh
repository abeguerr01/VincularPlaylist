#!/bin/bash

# Nombre del archivo que contiene las librerías
ARCHIVO_REQUISITOS="requeriments.txt"

echo "--- Iniciando comprobación de sistema ---"

# 1. Comprobar si Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 no está instalado. Intentando instalar..."
    
    # Intentamos instalarlo (asumiendo sistemas basados en Debian/Ubuntu como WSL)
    sudo apt update && sudo apt install -y python3 python3-pip
    
    if [ $? -ne 0 ]; then
        echo "[X] Error: No se pudo instalar Python. ¿Tienes permisos de sudo?"
        exit 1
    fi
else
    echo "[✓] Python3 ya está instalado."
fi

# 2. Comprobar si pip está instalado (a veces Python viene sin pip)
if ! command -v pip3 &> /dev/null; then
    echo "[!] Pip no encontrado. Instalando python3-pip..."
    sudo apt install -y python3-pip
fi

# 3. Verificar si el archivo .txt existe
if [ -f "$ARCHIVO_REQUISITOS" ]; then
    echo "--- Instalando librerías desde $ARCHIVO_REQUISITOS ---"
    pip3 install -r "$ARCHIVO_REQUISITOS"
    
    if [ $? -eq 0 ]; then
        echo "[✓] ¡Todo se instaló correctamente!"
    else
        echo "[X] Hubo un error instalando algunas librerías."
    fi
else
    echo "[X] Error: El archivo '$ARCHIVO_REQUISITOS' no existe."
    echo "Crea un archivo llamado $ARCHIVO_REQUISITOS con los nombres de las librerías."
fi