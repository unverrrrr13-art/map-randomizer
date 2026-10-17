from app.config import resource_path


def get_list(file_name: str) -> list[str]:
    try:
        with open(resource_path(file_name), 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f if line.strip()]
    except FileNotFoundError:
        return ["Файл не найден"]