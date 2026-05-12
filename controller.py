"""Controlador principal de la aplicación Pecibalto."""
import tkinter.filedialog
import tkinter.messagebox
from typing import Any, Optional

import config as cfg
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
        self._destination_path: str = ""
        self._current_format_key: str = cfg.DEFAULT_FORMAT

        self._wire_view_callbacks()

    def _wire_view_callbacks(self) -> None:
        """Conecta los callbacks de la vista al controller."""
        self._view.set_on_find_clicked(self.handle_find)
        self._view.set_on_download_clicked(self.handle_download)
        self._view.set_on_format_changed(self.handle_format_changed)
        self._view.set_on_browse_clicked(self.handle_browse_clicked)

    def _safe_update_ui(self, func, *args, **kwargs) -> None:
        """Helper para actualizar la UI desde un hilo de forma segura."""
        if hasattr(self._view, "root"):
            self._view.root.after(0, lambda: func(*args, **kwargs))

    def handle_find(self) -> None:
        """Maneja la acción de 'Encontrar'."""
        url = self._view.get_url()
        is_valid, error_msg = self._validator.validate(url)
        
        if not is_valid:
            self._view.show_error("Pecibalto", error_msg)
            return

        self._current_url = url
        self._view.find_button.set_enabled(False)

        def fetch_task():
            info = self._extractor.fetch_info(url)
            title = info.get("title", "Sin título")
            thumbnail_url = info.get("thumbnail")

            photo = None
            if thumbnail_url:
                photo = self._image_service.load_from_url(thumbnail_url)

            self._current_info = info

            self._safe_update_ui(self._view.set_title, title)
            if photo:
                self._safe_update_ui(self._view.set_thumbnail, photo)
            self._safe_update_ui(self._view.find_button.to_download)
            self._safe_update_ui(self._view.find_button.set_enabled, True)

        def on_error(exc: Exception):
            self._safe_update_ui(self._view.show_error, "Pecibalto", str(exc))
            self._safe_update_ui(self._view.find_button.set_enabled, True)

        self._thread_manager.run(target=fetch_task, on_error=on_error)

    def handle_download(self) -> None:
        """Maneja la acción de 'Descargar'."""
        if not self._current_url:
            return

        url = self._current_url
        format_key = self._view.get_selected_format()
        profile = cfg.FORMAT_PROFILES.get(format_key)
        if not profile:
            return

        output_path = self._view.get_destination_path()
        if not output_path:
            output_path = "."

        self._view.find_button.set_enabled(False)
        self._view.reset_progress()

        def download_task():
            self._extractor.download(
                url=url,
                output_path=output_path,
                format_profile=profile,
                progress_hook=self.handle_progress
            )

        def on_done():
            self._safe_update_ui(self._view.show_info, "Pecibalto", "Descarga completada.")
            self._safe_update_ui(self._view.reset)

        def on_error(exc: Exception):
            self._safe_update_ui(self._view.show_error, "Pecibalto", f"Error en descarga: {exc}")
            self._safe_update_ui(self._view.find_button.set_enabled, True)

        self._thread_manager.run(
            target=download_task,
            on_error=on_error,
            on_done=on_done
        )

    def handle_format_changed(self, format_key: str) -> None:
        """Maneja el cambio de formato."""
        self._current_format_key = format_key

    def handle_browse_clicked(self) -> None:
        """Maneja la selección de carpeta destino."""
        path = tkinter.filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if path:
            self._destination_path = path
            self._view.set_destination_path(path)

    def handle_progress(self, progress: float, data: dict) -> None:
        """Recibe actualizaciones de progreso de descarga."""
        self._safe_update_ui(self._view.set_progress, progress)

    def handle_error(self, error: Exception) -> None:
        """Maneja errores de servicios o hilos."""
        self._safe_update_ui(self._view.show_error, "Pecibalto", str(error))
        self._safe_update_ui(self._view.find_button.set_enabled, True)
