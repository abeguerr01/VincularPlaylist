@echo off
title Instalador de Python y Librerias
set ARCHIVO_REQUISITOS=requeriments.txt

echo =========================================
echo   COMPROBANDO PYTHON EN EL SISTEMA
echo =========================================

:: 1. Comprobar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python no encontrado. Intentando instalar via winget...
    
    :: Intentar instalar Python usando winget
    winget install -e --id Python.Python.3 --source winget --accept-package-agreements --accept-source-agreements
    
    if %errorlevel% neq 0 (
        echo [X] Error: No se pudo instalar Python. Asegurate de tener Windows 10 o 11.
        pause
        exit /b
    )
    echo [!] Python instalado. IMPORTANTE: Es posible que debas cerrar y abrir este script.
) else (
    echo [OK] Python ya esta instalado.
)

:: 2. Verificar si el archivo .txt existe
if exist %ARCHIVO_REQUISITOS% (
    echo.
    echo --- Instalando librerias desde %ARCHIVO_REQUISITOS% ---
    python -m pip install --upgrade pip
    python -m pip install -r %ARCHIVO_REQUISITOS%
    
    if %errorlevel% eq 0 (
        echo.
        echo [OK] ¡Todo se ha instalado correctamente!
    ) else (
        echo [X] Hubo un error al instalar las librerias.
    )
) else (
    echo [X] Error: No se encontro el archivo %ARCHIVO_REQUISITOS%.
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul