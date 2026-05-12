"""
Servicio de procesamiento de imágenes con Pillow.
"""
from typing import Any

from core.contracts import IImageService


class ImageService(IImageService):
    """Gestiona la carga, redimensionado y renderizado de miniaturas."""

    def load_from_url(self, image_url: str) -> Any:
        """Descarga y procesa una imagen remota para Tkinter."""
        raise NotImplementedError("Feature 3: Renderizado aún no implementado.")

    def resize(self, image: Any, width: int, height: int) -> Any:
        """Redimensiona una imagen manteniendo proporción."""
        raise NotImplementedError("Feature 3: Renderizado aún no implementado.")
