"""Controlador principal de la aplicación Pecibalto."""
from typing import Any, Optional

from core.contracts import (
    IExtractorService,
    IImageService,
    IThreadManager,
    ITraceLogger,
    IURLValidator,
)


class AppController:
    """Orquesta la interacción entre la UI y los servicios."""

    def __init__(
        self,
        view: Any,
        extractor: IExtractorService,
        image_service: IImageService,
        thread_manager: IThreadManager,
        validator: IURLValidator,
        logger: Optional[ITraceLogger] = None,
    ):
        self._view = view
        self._extractor = extractor
        self._image_service = image_service
        self._thread_manager = thread_manager
        self._validator = validator
        self._logger = logger

        self._current_info: Optional[dict] = None
        self._current_url: Optional[str] = None

        self._wire_view_callbacks()

    def _wire_view_callbacks(self) -> None:
        """Conecta los callbacks de la vista al controller."""
        self._view.set_on_find_clicked(self.handle_find)
        self._view.set_on_download_clicked(self.handle_download)
        self._view.set_on_format_changed(self.handle_format_changed)
        self._view.set_on_browse_clicked(self.handle_browse_clicked)

    def handle_find(self) -> None:
        """Maneja la acción de 'Encontrar'."""
        # Fase 4: implementar wiring real.
        pass

    def handle_download(self) -> None:
        """Maneja la acción de 'Descargar'."""
        # Fase 4: implementar wiring real.
        pass

    def handle_format_changed(self, format_key: str) -> None:
        """Maneja el cambio de formato."""
        # Fase 4: implementar wiring real.
        pass

    def handle_browse_clicked(self) -> None:
        """Maneja la selección de carpeta destino."""
        # Fase 4: implementar wiring real.
        pass

    def handle_progress(self, progress: float, data: dict) -> None:
        """Recibe actualizaciones de progreso de descarga."""
        # Fase 4: implementar wiring real.
        pass

    def handle_error(self, error: Exception) -> None:
        """Maneja errores de servicios o hilos."""
        # Fase 4: implementar wiring real.
        pass
