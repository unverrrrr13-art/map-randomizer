import os

APP_NAME = "Рандомайзер"
WINDOW_TITLE = "Рандомайзер"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Ресурсы (пути относительно корня проекта)
MAPS_FILE = os.path.join("assets", "data", "maps.txt")
TIMES_FILE = os.path.join("assets", "data", "time.txt")
WEATHER_FILE = os.path.join("assets", "data", "weather.txt")
IMAGE_FILE = os.path.join("assets", "images", "image.png")

# Цвета
BACKGROUND_COLOR = "#1a1a1a"


def get_base_path() -> str:
    """Корень проекта — директория, содержащая app/ и assets/."""
    # config.py лежит в app/, поднимаемся на уровень выше
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resource_path(name: str) -> str:
    return os.path.join(get_base_path(), name)