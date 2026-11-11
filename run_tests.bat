@echo off
chcp 65001 > nul
title Taller de Pruebas Automatizadas
echo ==============================================================
echo    EJECUTOR DE PRUEBAS AUTOMATIZADAS - TALLER UNIVERSITARIO
echo ==============================================================
echo.

if not exist venv (
    echo [AVISO] No se encontro el entorno virtual 'venv'.
    echo Creando entorno virtual e instalando librerias necesarias...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .\venv\Scripts\activate.bat
)

echo.
echo --------------------------------------------------------------
echo  [Paso 1 de 2] Ejecutando pruebas de API REST (Requests + Pytest)
echo --------------------------------------------------------------
python -m pytest tests/api/test_api_rest.py -v
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ALERTA] Se detectaron errores en las pruebas de API.
) else (
    echo.
    echo [EXITO] Todas las pruebas de API finalizaron correctamente.
)

echo.
echo --------------------------------------------------------------
echo  [Paso 2 de 2] Ejecutando pruebas de Formulario Web (Selenium)
echo --------------------------------------------------------------
echo Nota: Para ejecutar sin abrir la ventana del navegador, use:
echo       python -m pytest tests/ui/test_web_form.py --headless
echo.
python -m pytest tests/ui/test_web_form.py -v
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ALERTA] Se detectaron errores en las pruebas de Formulario Web.
) else (
    echo.
    echo [EXITO] Todas las pruebas de Formulario Web finalizaron correctamente.
)

echo.
echo ==============================================================
echo   EJECUCION FINALIZADA. EVIDENCIAS DISPONIBLES EN /evidencias
echo ==============================================================
echo.
pause
