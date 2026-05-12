"""
Servicio de extracción de medios basado en yt-dlp.
"""


class ExtractorService:
    """Encapsula la lógica de extracción de información y descarga con yt-dlp."""

    def __init__(self):
        pass

    def fetch_info(self, url):
        """Obtiene metadatos sin descargar (extract_info con download=False)."""
        pass

    def download(self, url, output_path, format_profile, progress_hook):
        """Ejecuta la descarga del medio."""
        pass
