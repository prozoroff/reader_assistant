from pathlib import Path
from typing import Final

# Путь к файлу с текстом
BASE_DIR: Final[Path] = Path(__file__).parent
DATA_DIR: Final[Path] = BASE_DIR / "data"
FILE_PATH: Final[Path] = DATA_DIR / "dairy.txt"

# Настройки текстового сплиттера
TEXT_SPLITTER_CHUNK_SIZE: Final[int] = 1000
TEXT_SPLITTER_OVERLAP: Final[int] = 100

# Настройки Yandex API
import os

YANDEX_API_KEY: Final[str] = os.environ["YANDEX_API_KEY"]
YANDEX_FOLDER_ID: Final[str] = os.environ["YANDEX_FOLDER_ID"] 
YANDEX_GEOCODER_API_KEY: Final[str] = os.environ["YANDEX_GEOCODER_API_KEY"]

# Настройки эмбеддингов
EMBEDDINGS_BATCH_SIZE: Final[int] = 5
EMBEDDINGS_DELAY_BETWEEN_BATCHES: Final[float] = 0.5

# Настройки поиска
SEARCH_K: Final[int] = 3 
