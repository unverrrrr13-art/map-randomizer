import sys

from PySide6.QtWidgets import QApplication

from app.ui import BusinessRandomizerApp
from app.config import STYLE_FILE, resource_path # <- Добавили импорт

def main():
    app = QApplication(sys.argv)
    
    # Читаем и применяем QSS
    try:
        with open(resource_path(STYLE_FILE), "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Файл стилей не найден, используем стандартные.")

    win = BusinessRandomizerApp()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()