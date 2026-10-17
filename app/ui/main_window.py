import os
import random

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from app.config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_FILE,
    MAPS_FILE, TIMES_FILE, WEATHER_FILE, resource_path
)
from app.data_loader import get_list
from app.widgets import GradientImageLabel


class BusinessRandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.maps = get_list(MAPS_FILE)
        self.times = get_list(TIMES_FILE)
        self.weather = get_list(WEATHER_FILE)

        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self._build_ui()
        self.setFocusPolicy(Qt.StrongFocus)

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background: #1a1a1a;")

        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        self.image_label = GradientImageLabel()
        self.image_label.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.load_image(IMAGE_FILE)
        main_layout.addWidget(self.image_label, 0, 0, 1, 1)

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(60, 40, 40, 40)
        content_layout.setSpacing(20)

        # Заголовок
        title_container = QWidget()
        title_container.setStyleSheet("background: transparent;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(80, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Подпольная федерация танководства")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 20px;
            background: transparent;
            padding: 10px 0;
        """)
        title_layout.addWidget(self.title_label)

        content_layout.addWidget(title_container)

        # Результаты
        results_wrapper = QWidget()
        results_wrapper.setStyleSheet("background: transparent;")
        results_wrapper_layout = QHBoxLayout(results_wrapper)
        results_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        results_wrapper_layout.setSpacing(0)

        self.results_container = QWidget()
        self.results_container.setStyleSheet("background: transparent;")
        results_layout = QVBoxLayout(self.results_container)
        results_layout.setSpacing(12)
        results_layout.setContentsMargins(230, 0, 0, 0)

        results_wrapper_layout.addWidget(self.results_container)
        results_wrapper_layout.addStretch()

        content_layout.addWidget(results_wrapper)

        self.show_empty_results()

        # Кнопка
        button_wrapper = QWidget()
        button_wrapper.setStyleSheet("background: transparent;")
        button_wrapper_layout = QHBoxLayout(button_wrapper)
        button_wrapper_layout.setContentsMargins(300, 0, 0, 0)
        button_wrapper_layout.setSpacing(0)

        self.button = QPushButton("Сгенерировать")
        self.button.clicked.connect(self.update_results)
        self.button.setFixedSize(150, 37)
        self.button.setStyleSheet("""
            QPushButton {
                background: #383838;
                color: #ffffff;
                border: 1px solid #727272;
                border-radius: 8px;
                font-size: 16px;
                padding: 7px 10px;
            }
            QPushButton:hover {
                background: #505050;
            }
            QPushButton:pressed {
                background: rgba(100, 100, 100, 0.9);
            }
        """)

        button_wrapper_layout.addWidget(self.button)
        button_wrapper_layout.addStretch()

        content_layout.addWidget(button_wrapper)
        content_layout.addStretch()

        main_layout.addWidget(content_widget, 0, 0, 1, 1)

    def load_image(self, image_path: str):
        try:
            full_path = resource_path(image_path)
            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                if not pixmap.isNull():
                    self.image_label.setPixmap(pixmap)
                    return
            self.show_placeholder()
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")

    def show_placeholder(self):
        """Заглушка, если картинки нет или она не загрузилась."""
        self.image_label.clear_pixmap()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.update_results()

    def create_result_row(self, label_text: str, value: str, is_empty: bool = False) -> QWidget:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        row.setFixedHeight(35)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(15)

        label = QLabel(label_text)
        label.setFixedWidth(60)
        label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.7); font-size: 14px; background: transparent;"
        )

        value_label = QLabel(value)
        if is_empty:
            value_label.setStyleSheet(
                "color: rgba(255, 255, 255, 0.4); font-size: 14px; "
                "font-style: italic; background: transparent;"
            )
        else:
            value_label.setStyleSheet(
                "color: #ffffff; font-size: 14px; background: transparent;"
            )

        value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        value_label.setWordWrap(False)

        row_layout.addWidget(label, alignment=Qt.AlignLeft)
        row_layout.addWidget(value_label, alignment=Qt.AlignLeft)
        row_layout.addStretch()

        return row

    def _clear_results(self):
        layout = self.results_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_empty_results(self):
        self._clear_results()
        for label_text in ("Карта", "Время", "Погода"):
            self.results_container.layout().addWidget(
                self.create_result_row(label_text, "—", is_empty=True)
            )

    def update_results(self):
        self._clear_results()

        map_value = random.choice(self.maps) if self.maps else "Нет данных"
        time_value = random.choice(self.times) if self.times else "Нет данных"
        weather_value = random.choice(self.weather) if self.weather else "Нет данных"

        items = [
            ("Карта", map_value),
            ("Время", time_value),
            ("Погода", weather_value),
        ]

        for label_text, value in items:
            self.results_container.layout().addWidget(
                self.create_result_row(label_text, value, is_empty=False)
            )