import sys
from PySide6.QtWidgets import QApplication
from app.ui import BusinessRandomizerApp
from app.config import resource_path, STYLE_FILE

def main():
    app = QApplication(sys.argv)
   
    style_path = resource_path(STYLE_FILE)
    try:
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Файл стилей не найден по пути: {style_path}")

    win = BusinessRandomizerApp()
    win.show()
    sys.exit(app.exec())