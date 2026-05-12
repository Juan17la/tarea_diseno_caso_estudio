"""
Servicio de procesamiento de imágenes con Pillow.
"""
import requests
from io import BytesIO
from typing import Any
from PIL import Image, ImageTk

from core.contracts import IImageService


class ImageService(IImageService):
    """Gestiona la carga, redimensionado y renderizado de miniaturas."""

    def load_from_url(self, image_url: str) -> Any:
        """Descarga y procesa una imagen remota para Tkinter."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            img = self.resize(img, 320, 180)
            
            return ImageTk.PhotoImage(img)
        except Exception as e:
            raise ValueError(f"No se pudo cargar la imagen desde la URL: {e}")

    def resize(self, image: Any, width: int, height: int) -> Any:
        """Redimensiona una imagen manteniendo proporción."""
        # Use Image.Resampling.LANCZOS if available, fallback to Image.ANTIALIAS
        resample_filter = getattr(Image, "Resampling", Image).LANCZOS
        
        # Calculate aspect ratio preserving dimensions
        image.thumbnail((width, height), resample_filter)
        return image
