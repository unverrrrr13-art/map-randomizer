import sys

from PySide6.QtWidgets import QApplication

from app.ui import BusinessRandomizerApp


def main():
    app = QApplication(sys.argv)
    win = BusinessRandomizerApp()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()