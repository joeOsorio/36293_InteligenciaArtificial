@echo off
REM =============================================================
REM  run.bat
REM  Activa el entorno virtual y lanza el proyecto BFS.
REM  Coloca este archivo en la raiz del proyecto (junto a src/).
REM =============================================================

call venv_BFS\Scripts\activate.bat
python src\bfs_mapa\main.py
pause
