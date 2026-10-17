import os
import random

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from app.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_FILE,
    MAPS_FILE, MAPS_WTLIVE_FILE, TIMES_FILE, WEATHER_FILE, resource_path
)
from app.data_loader import get_list
from app.widgets import GradientImageLabel
from app import texts


class BusinessRandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.maps = get_list(MAPS_FILE)
        self.maps_wtlive = get_list(MAPS_WTLIVE_FILE)
        self.times = get_list(TIMES_FILE)
        self.weather = get_list(WEATHER_FILE)

        self.setWindowTitle(texts.WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self._build_ui()
        self.setFocusPolicy(Qt.StrongFocus)

    def _build_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

        # Главный слой (сетка) для фона и контента
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # 1. Фоновая картинка
        self.image_label = GradientImageLabel()
        self.image_label.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.load_image(IMAGE_FILE)
        main_layout.addWidget(self.image_label, 0, 0, 1, 1)

        # 2. Основной контент
        content_widget = QWidget()
        content_widget.setObjectName("transparent_widget")
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(60, 40, 40, 20)
        content_layout.setSpacing(15)

        # Заголовок
        title_container = QWidget()
        title_container.setObjectName("transparent_widget")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(80, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel(texts.MAIN_TITLE)
        self.title_label.setObjectName("main_title")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)

        content_layout.addWidget(title_container)

        # Результаты
        results_wrapper = QWidget()
        results_wrapper.setObjectName("transparent_widget")
        results_wrapper_layout = QHBoxLayout(results_wrapper)
        results_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        results_wrapper_layout.setSpacing(0)

        self.results_container = QWidget()
        self.results_container.setObjectName("transparent_widget")
        results_layout = QVBoxLayout(self.results_container)
        results_layout.setSpacing(12)
        results_layout.setContentsMargins(230, 0, 0, 0)

        results_wrapper_layout.addWidget(self.results_container)
        results_wrapper_layout.addStretch()

        content_layout.addWidget(results_wrapper)

        self.show_empty_results()

        # Кнопка "Сгенерировать"
        button_wrapper = QWidget()
        button_wrapper.setObjectName("transparent_widget")
        button_wrapper_layout = QHBoxLayout(button_wrapper)
        button_wrapper_layout.setContentsMargins(300, 0, 0, 0)
        button_wrapper_layout.setSpacing(0)

        self.button = QPushButton(texts.BTN_GENERATE)
        self.button.setObjectName("generate_btn")
        self.button.clicked.connect(self.update_all_results)
        self.button.setFixedSize(150, 37)

        button_wrapper_layout.addWidget(self.button)
        button_wrapper_layout.addStretch()

        content_layout.addWidget(button_wrapper)
        content_layout.addStretch()

        main_layout.addWidget(content_widget, 0, 0, 1, 1)

        # 3. Чекбокс (абсолютное позиционирование поверх окна)
        self.chk_wt_live = QCheckBox(texts.CHK_WT_LIVE, central_widget)
        self.chk_wt_live.setObjectName("wt_live_chk")
        self.chk_wt_live.setCursor(Qt.PointingHandCursor)
        
        self.chk_wt_live.adjustSize()
        
        x_pos = WINDOW_WIDTH - self.chk_wt_live.width() - 20
        y_pos = WINDOW_HEIGHT - self.chk_wt_live.height() - 20
        
        self.chk_wt_live.move(x_pos, y_pos)
        self.chk_wt_live.raise_()

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
        self.image_label.clear_pixmap()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.update_all_results()

    def create_result_row(self, label_text: str, value: str, is_empty: bool = False, callback=None) -> QWidget:
        row = QWidget()
        row.setObjectName("transparent_widget")
        row.setFixedHeight(35)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(15)

        btn_label = QPushButton(label_text)
        btn_label.setObjectName("param_btn")
        btn_label.setFixedWidth(60)
        btn_label.setCursor(Qt.PointingHandCursor)
        
        if callback:
            btn_label.clicked.connect(callback)

        value_label = QLabel(value)
        value_label.setObjectName("value_label_empty" if is_empty else "value_label")
        
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

    def _get_random_map(self):
        """Выбирает случайную карту. Если галочка стоит - объединяет оба списка."""
        if self.chk_wt_live.isChecked() and self.maps_wtlive:
            # Объединяем основной список и WT Live
            combined_maps = self.maps + self.maps_wtlive
            return random.choice(combined_maps)
        
        # Если галочка не стоит, берем только обычные карты
        return random.choice(self.maps) if self.maps else texts.ERROR_NO_DATA

    def _get_random_value(self, data_list):
        return random.choice(data_list) if data_list else texts.ERROR_NO_DATA

    def show_empty_results(self):
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
        self._clear_results()

        items = [
            (texts.LABEL_MAP, self._get_random_map(), lambda: self.update_single_result("map")),
            (texts.LABEL_TIME, self._get_random_value(self.times), lambda: self.update_single_result("time")),
            (texts.LABEL_WEATHER, self._get_random_value(self.weather), lambda: self.update_single_result("weather"))
        ]

        for label_text, value, callback in items:
            self.results_container.layout().addWidget(
                self.create_result_row(label_text, value, is_empty=False, callback=callback)
            )

    def update_single_result(self, result_type: str):
        layout = self.results_container.layout()
        
        if result_type == "map":
            new_value = self._get_random_map()
            index = 0
        elif result_type == "time":
            new_value = self._get_random_value(self.times)
            index = 1
        else:
            new_value = self._get_random_value(self.weather)
            index = 2

        item = layout.itemAt(index)
        if not item or not item.widget():
            return
            
        row_widget = item.widget()
        row_layout = row_widget.layout()
        value_label = row_layout.itemAt(1).widget()
        
        if isinstance(value_label, QLabel):
            value_label.setText(new_value)
            value_label.setObjectName("value_label")
            value_label.style().unpolish(value_label)
            value_label.style().polish(value_label)