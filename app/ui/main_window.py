import os
import random

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QCheckBox, QApplication, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap

from app.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_FILE,
    MAPS_FILE, MAPS_WTLIVE_FILE, TIMES_FILE, WEATHER_FILE, 
    WTLIVE_PREFIX, resource_path
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

        self.current_map_value = None 
        self.current_map_is_wtlive = False

        self._build_ui()
        self.setFocusPolicy(Qt.StrongFocus)

    def _build_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

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

        # 3. Чекбокс (абсолютное позиционирование)
        self.chk_wt_live = QCheckBox(texts.CHK_WT_LIVE, central_widget)
        self.chk_wt_live.setObjectName("wt_live_chk")
        self.chk_wt_live.setCursor(Qt.PointingHandCursor)
        self.chk_wt_live.adjustSize()
        
        x_pos = WINDOW_WIDTH - self.chk_wt_live.width() - 20
        y_pos = WINDOW_HEIGHT - self.chk_wt_live.height() - 20
        
        self.chk_wt_live.move(x_pos, y_pos)
        self.chk_wt_live.raise_()

        # 4. Маркер "Скопировано" (левый нижний угол) с анимацией
        self.copy_marker = QLabel(texts.COPY_MARKER, central_widget)
        self.copy_marker.setObjectName("copy_marker")
        self.copy_marker.setStyleSheet("color: #a0a0a0; font-size: 12px; background: transparent;")
        self.copy_marker.adjustSize()
        
        marker_y = WINDOW_HEIGHT - self.copy_marker.height() - 20
        self.copy_marker.move(20, marker_y)

        # Настройка эффекта прозрачности
        self.opacity_effect = QGraphicsOpacityEffect(self.copy_marker)
        self.copy_marker.setGraphicsEffect(self.opacity_effect)

        # Настройка анимации
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1500) # 1.5 секунды
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Скрываем маркер, когда анимация завершится
        self.fade_animation.finished.connect(self.copy_marker.hide)
        
        self.copy_marker.hide()

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

    def create_result_row(self, label_text: str, value: str, is_empty: bool = False, callback=None, value_callback=None) -> QWidget:
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

        if value_callback:
            value_widget = QPushButton(value)
            value_widget.setObjectName("value_label_empty" if is_empty else "value_label")
            value_widget.setStyleSheet("text-align: left; border: none; background: transparent; padding: 0;")
            value_widget.setCursor(Qt.PointingHandCursor)
            value_widget.clicked.connect(lambda: value_callback(value_widget))
        else:
            value_widget = QLabel(value)
            value_widget.setObjectName("value_label_empty" if is_empty else "value_label")
            value_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            value_widget.setWordWrap(False)

        row_layout.addWidget(btn_label, alignment=Qt.AlignLeft)
        row_layout.addWidget(value_widget, alignment=Qt.AlignLeft)
        row_layout.addStretch()

        return row

    def _clear_results(self):
        layout = self.results_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _get_random_map(self):
        """Возвращает кортеж (текст_для_отображения, оригинал_строки, это_wtlive)"""
        if self.chk_wt_live.isChecked():
            # Объединяем оба списка
            combined_maps = self.maps + self.maps_wtlive
            if not combined_maps:
                return texts.ERROR_NO_DATA, texts.ERROR_NO_DATA, False
                
            raw_map = random.choice(combined_maps)
            is_wtlive = raw_map in self.maps_wtlive
            
            # Отрезаем всё после ' | ' для отображения
            display_text = raw_map.split(' | ')[0].strip()
            
            if is_wtlive:
                display_text = f"{WTLIVE_PREFIX}{display_text}"
                
            return display_text, raw_map, is_wtlive
        
        # Если галочка не стоит, берем только из обычных карт
        if not self.maps:
            return texts.ERROR_NO_DATA, texts.ERROR_NO_DATA, False
            
        raw_map = random.choice(self.maps)
        display_text = raw_map.split(' | ')[0].strip()
        
        return display_text, raw_map, False

    def _get_random_value(self, data_list):
        """Для времени и погоды тоже отрезаем ' | ' на всякий случай"""
        if not data_list:
            return texts.ERROR_NO_DATA
        raw_val = random.choice(data_list)
        return raw_val.split(' | ')[0].strip()

    def _process_map_click(self, label_widget):
        """Копирует ссылку и показывает маркер в левом нижнем углу."""
        if not self.current_map_value or not self.current_map_is_wtlive:
            return

        # Ищем разделитель ' | '
        if ' | ' in self.current_map_value:
            parts = self.current_map_value.split(' | ', 1)
            if len(parts) > 1 and parts[1].strip():
                link = parts[1].strip()
                clipboard = QApplication.clipboard()
                clipboard.setText(link)
                
                # Показываем маркер
                self.copy_marker.show()
                
                # Сбрасываем прозрачность (если предыдущая анимация не доделала до конца)
                self.opacity_effect.setOpacity(1.0)
                
                # Запускаем плавное исчезновение
                self.fade_animation.start()

    def show_empty_results(self):
        self._clear_results()
        self.current_map_value = None
        
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

        map_display, map_raw, is_wtlive = self._get_random_map()
        self.current_map_value = map_raw
        self.current_map_is_wtlive = is_wtlive

        items = [
            (texts.LABEL_MAP, map_display, lambda: self.update_single_result("map"), True),
            (texts.LABEL_TIME, self._get_random_value(self.times), lambda: self.update_single_result("time"), False),
            (texts.LABEL_WEATHER, self._get_random_value(self.weather), lambda: self.update_single_result("weather"), False)
        ]

        for label_text, value, callback, is_map in items:
            row = self.create_result_row(
                label_text, 
                value, 
                is_empty=False, 
                callback=callback,
                value_callback=self._process_map_click if is_map else None
            )
            self.results_container.layout().addWidget(row)

    def update_single_result(self, result_type: str):
        layout = self.results_container.layout()
        
        if result_type == "map":
            display_val, raw_val, is_wtlive = self._get_random_map()
            self.current_map_value = raw_val
            self.current_map_is_wtlive = is_wtlive
            index = 0
        elif result_type == "time":
            display_val = self._get_random_value(self.times)
            index = 1
        else:
            display_val = self._get_random_value(self.weather)
            index = 2

        item = layout.itemAt(index)
        if not item or not item.widget():
            return
            
        row_widget = item.widget()
        row_layout = row_widget.layout()
        value_widget = row_layout.itemAt(1).widget()
        
        if result_type == "map":
            # Пересоздаем виджет, так как меняется кликабельность
            value_widget.deleteLater()
            
            value_btn = QPushButton(display_val)
            value_btn.setObjectName("value_label")
            value_btn.setStyleSheet("text-align: left; border: none; background: transparent; padding: 0;")
            value_btn.setCursor(Qt.PointingHandCursor)
            value_btn.clicked.connect(lambda: self._process_map_click(value_btn))
            
            row_layout.insertWidget(1, value_btn, alignment=Qt.AlignLeft)
        else:
            if isinstance(value_widget, QLabel):
                value_widget.setText(display_val)
                value_widget.setObjectName("value_label")
                value_widget.style().unpolish(value_widget)
                value_widget.style().polish(value_widget)
            elif isinstance(value_widget, QPushButton):
                value_widget.setText(display_val)