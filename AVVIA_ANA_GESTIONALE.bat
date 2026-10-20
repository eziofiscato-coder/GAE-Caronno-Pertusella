@echo off
title ANA Gestionale Varese - Avvio
color 0A
echo ========================================
echo  ANA Gestionale Varese - Caronno Pertusella
echo  Avvio Dashboard Volontari
echo ========================================
echo.

REM Vai nella cartella dello script
cd /d "%~dp0"

echo [1/3] Verifica Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERRORE: Python non trovato!
    echo.
    echo Installa Python:
    echo 1. Vai su https://www.python.org/downloads/
    echo 2. Scarica Python 3.11 o 3.12
    echo 3. Installa SPUNTANDO "Add python.exe to PATH"
    echo 4. Riavvia questo file .bat
    echo.
    pause
    exit /b
)
python --version

echo.
echo [2/3] Verifica librerie...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installo librerie da requirements.txt...
    pip install -r requirements.txt
    echo Librerie installate!
) else (
    echo Librerie OK!
)

echo.
echo [3/3] Avvio ANA Gestionale...
echo Si aprira il browser su http://localhost:8501
echo Non chiudere questa finestra!
echo Per chiudere: Ctrl+C in questa finestra
echo.
echo ========================================
timeout /t 2 >nul

streamlit run app.py --server.port 8501 --server.headless false --browser.gatherUsageStats false

echo.
echo App chiusa.
pause
