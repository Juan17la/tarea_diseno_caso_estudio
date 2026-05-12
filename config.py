"""Constantes y configuración centralizada de Pecibalto."""

from pathlib import Path

# UI
APP_NAME = "Pecibalto"
APP_SUBTITLE = "Universal Media Extractor"
WINDOW_MIN_WIDTH = 500
WINDOW_MIN_HEIGHT = 300
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400

# Colores
BG_PRIMARY = "#f5f6fa"
BG_CARD = "#ffffff"
TEXT_PRIMARY = "#2f3640"
TEXT_SECONDARY = "#718093"
ACCENT = "#007bff"
ACCENT_HOVER = "#0069d9"
ACCENT_ACTIVE = "#0056b3"
BORDER = "#ccc"
PLACEHOLDER_FG = "#999"

# Fuentes
FONT_FAMILY = "Helvetica"
FONT_TITLE = (FONT_FAMILY, 28, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 12)
FONT_INPUT = (FONT_FAMILY, 11)
FONT_BUTTON = (FONT_FAMILY, 10, "bold")

# Placeholders
URL_PLACEHOLDER = "Pega aquí tu enlace..."

# Formatos
FORMAT_PROFILES = {
    "MP4 (Video)": {"profile": "mp4", "ext": "mp4"},
    "MP3 (Audio)": {"profile": "mp3", "ext": "mp3"},
}

DEFAULT_FORMAT = "MP4 (Video)"

# Logging
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pecibalto.log"
LOG_LEVEL = "INFO"
