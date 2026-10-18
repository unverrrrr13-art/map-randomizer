@echo off
chcp 65001 >nul
cd /d "%~dp0"

python -c "import PySide6" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Installing dependencies...
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b
    )
)

echo Starting GuP Randomizer...
start "" pythonw -m app.main

exit