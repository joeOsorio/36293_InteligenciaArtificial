@echo off
REM =============================================================
REM  setup_venv.bat
REM  Crea el entorno virtual "venv_BFS" e instala solo las
REM  dependencias necesarias para ejecutar el proyecto.
REM
REM  Uso: Doble clic en el archivo, o desde terminal:
REM       setup_venv.bat
REM =============================================================

echo.
echo =============================================
echo  Configurando entorno virtual para BFS Mapa
echo =============================================
echo.

REM ── 1. Crear el entorno virtual ──────────────────────────────
echo [1/4] Creando entorno virtual "venv_BFS"...
python -m venv venv_BFS

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: No se pudo crear el entorno virtual.
    echo Asegurate de tener Python instalado y en el PATH.
    pause
    exit /b 1
)
echo       OK
echo.

REM ── 2. Activar el entorno virtual ────────────────────────────
echo [2/4] Activando entorno virtual...
call venv_BFS\Scripts\activate.bat

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: No se pudo activar el entorno virtual.
    pause
    exit /b 1
)
echo       OK
echo.

REM ── 3. Actualizar pip ────────────────────────────────────────
echo [3/4] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo       OK
echo.

REM ── 4. Instalar dependencias del proyecto ────────────────────
echo [4/4] Instalando dependencias...
echo.

REM  pygame — unica dependencia real del proyecto
pip install pygame==2.6.1

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: No se pudo instalar pygame.
    pause
    exit /b 1
)

echo.
echo =============================================
echo  Entorno listo.
echo.
echo  Para ejecutar el proyecto:
echo.
echo    venv_BFS\Scripts\activate
echo    python src\bfs_mapa\main.py
echo.
echo  O usa el acceso directo:
echo    run.bat
echo =============================================
echo.
pause
