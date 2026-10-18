#!/bin/bash
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python 3 не установлен. Установите его через пакетный менеджер (например, sudo apt install python3)."
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

if ! python3 -c "import PySide6" &> /dev/null; then
    echo "[INFO] PySide6 не найден. Устанавливаем зависимости..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ОШИБКА] Не удалось установить зависимости. Проверьте подключение к интернету и права доступа."
        read -p "Нажмите Enter для выхода..."
        exit 1
    fi
fi

echo "Запуск Map Randomizer..."
python3 -m app.main

if [ $? -ne 0 ]; then
    echo ""
    echo "[ОШИБКА] Программа завершилась с ошибкой."
    read -p "Нажмите Enter для выхода..."
fi