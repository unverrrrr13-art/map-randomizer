import os

APP_NAME = "Рандомайзер"
WINDOW_TITLE = "Рандомайзер"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

MAPS_FILE = os.path.join("assets", "data", "maps.txt")
TIMES_FILE = os.path.join("assets", "data", "time.txt")
WEATHER_FILE = os.path.join("assets", "data", "weather.txt")
IMAGE_FILE = os.path.join("assets", "images", "image.png")

# Добавили путь к файлу стилей
STYLE_FILE = os.path.join("app", "style.qss")

BACKGROUND_COLOR = "#1a1a1a"

def get_base_path() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resource_path(name: str) -> str:
    return os.path.join(get_base_path(), name)