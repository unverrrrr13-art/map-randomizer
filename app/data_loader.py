from app.config import resource_path
from app import texts

def get_list(file_name: str) -> list[str]:
    try:
        with open(resource_path(file_name), 'r', encoding='utf-8') as f:
            return [
                line.rstrip('\n').strip() 
                for line in f 
                if line.strip() and not line.strip().startswith('//')
            ]
    except FileNotFoundError:
        return [texts.ERROR_FILE_NOT_FOUND]