from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor


class GradientImageLabel(QLabel):
    """Кастомный QLabel с градиентным переходом в прозрачность."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None
        self.setMinimumSize(250, 100)
        self.setStyleSheet("background: #1a1a1a;")

    def setPixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self.update()

    def clear_pixmap(self):
        """Сбрасывает изображение (используется как заглушка)."""
        self._pixmap = None
        self.update()

    def paintEvent(self, event):
        if self._pixmap is None or self._pixmap.isNull():
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        scaled_pixmap = self._pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        offset_x = -150
        offset_y = 0

        x = (self.width() - scaled_pixmap.width()) // 2 + offset_x
        y = (self.height() - scaled_pixmap.height()) // 2 + offset_y

        painter.drawPixmap(x, y, scaled_pixmap)

        gradient = QLinearGradient(self.rect().topLeft(), self.rect().topRight())
        gradient.setColorAt(0.0, QColor(26, 26, 26, 0))
        gradient.setColorAt(0.35, QColor(26, 26, 26, 200))
        gradient.setColorAt(0.55, QColor(26, 26, 26, 255))

        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.fillRect(self.rect(), gradient)

        painter.end()