@echo off
chcp 65001 >nul
cd /d "%~dp0"

python -c "import PySide6" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] PySide6 не найден. Устанавливаем зависимости...
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo.
        echo [ОШИБКА] Не удалось установить зависимости. 
        echo Убедитесь, что Python установлен и добавлен в PATH.
        pause
        exit /b
    )
)

echo Запуск Map Randomizer...
python -m app.main

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ОШИБКА] Программа завершилась с ошибкой.
    pause
)