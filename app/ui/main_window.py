import os
import random

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from app.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_FILE,
    MAPS_FILE, TIMES_FILE, WEATHER_FILE, resource_path
)
from app.data_loader import get_list
from app.widgets import GradientImageLabel
from app import texts


class BusinessRandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.maps = get_list(MAPS_FILE)
        self.times = get_list(TIMES_FILE)
        self.weather = get_list(WEATHER_FILE)

        self.setWindowTitle(texts.WINDOW_TITLE)
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

        self.title_label = QLabel(texts.MAIN_TITLE)
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

        self.button = QPushButton(texts.BTN_GENERATE)
        self.button.clicked.connect(self.update_all_results)
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
            self.update_all_results()

    def create_result_row(self, label_text: str, value: str, is_empty: bool = False, callback=None) -> QWidget:
        """Создает строку. Если передан callback, текст слева становится кнопкой."""
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        row.setFixedHeight(35)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(15)

        # Вместо QLabel используем QPushButton
        btn_label = QPushButton(label_text)
        btn_label.setFixedWidth(60)
        btn_label.setCursor(Qt.PointingHandCursor) # Курсор в виде руки
        
        # Стили для кнопки (выглядят как текст, но реагируют на наведение)
        btn_label.setStyleSheet("""
            QPushButton {
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                background: transparent;
                border: none;
                text-align: left;
                padding: 0;
            }
            QPushButton:hover {
                color: rgba(255, 255, 255, 1.0); /* Светлеет при наведении */
            }
            QPushButton:pressed {
                color: rgba(200, 200, 200, 1.0);
            }
        """)
        
        # Привязываем функцию, если она передана
        if callback:
            btn_label.clicked.connect(callback)

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

        row_layout.addWidget(btn_label, alignment=Qt.AlignLeft)
        row_layout.addWidget(value_label, alignment=Qt.AlignLeft)
        row_layout.addStretch()

        return row

    def _clear_results(self):
        layout = self.results_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _get_random_value(self, data_list):
        """Вспомогательный метод для получения значения или ошибки."""
        return random.choice(data_list) if data_list else texts.ERROR_NO_DATA

    def show_empty_results(self):
        """Показывает пустые значения (—) при запуске."""
        self._clear_results()
        
        items = [
            (texts.LABEL_MAP, texts.EMPTY_VALUE, lambda: self.update_single_result("map")),
            (texts.LABEL_TIME, texts.EMPTY_VALUE, lambda: self.update_single_result("time")),
            (texts.LABEL_WEATHER, texts.EMPTY_VALUE, lambda: self.update_single_result("weather"))
        ]
        
        for label_text, value, callback in items:
            self.results_container.layout().addWidget(
                self.create_result_row(label_text, value, is_empty=True, callback=callback)
            )

    def update_all_results(self):
        """Обновляет все три значения (вызывается кнопкой 'Сгенерировать')."""
        self._clear_results()

        items = [
            (texts.LABEL_MAP, self._get_random_value(self.maps), lambda: self.update_single_result("map")),
            (texts.LABEL_TIME, self._get_random_value(self.times), lambda: self.update_single_result("time")),
            (texts.LABEL_WEATHER, self._get_random_value(self.weather), lambda: self.update_single_result("weather"))
        ]

        for label_text, value, callback in items:
            self.results_container.layout().addWidget(
                self.create_result_row(label_text, value, is_empty=False, callback=callback)
            )

    def update_single_result(self, result_type: str):
        """Обновляет только одно значение (вызывается кликом по тексту слева)."""
        layout = self.results_container.layout()
        
        if result_type == "map":
            data = self.maps
            index = 0
        elif result_type == "time":
            data = self.times
            index = 1
        else:
            data = self.weather
            index = 2

        item = layout.itemAt(index)
        if not item or not item.widget():
            return
            
        row_widget = item.widget()
        row_layout = row_widget.layout()
        value_label = row_layout.itemAt(1).widget()
        
        if isinstance(value_label, QLabel):
            new_value = self._get_random_value(data)
            value_label.setText(new_value)
            value_label.setStyleSheet("color: #ffffff; font-size: 14px; background: transparent;")