"""Contratos (Protocols) para la arquitectura de Pecibalto."""
from typing import Any, Callable, Optional, Protocol, Tuple, runtime_checkable


@runtime_checkable
class IExtractorService(Protocol):
    """Contrato para extracción de metadatos y descarga."""

    def fetch_info(self, url: str) -> dict:
        """Obtiene metadatos sin descargar."""
        ...

    def download(
        self,
        url: str,
        output_path: str,
        format_profile: Any,
        progress_hook: Optional[Callable[[float, dict], None]] = None,
    ) -> dict:
        """Ejecuta la descarga del medio."""
        ...


@runtime_checkable
class IImageService(Protocol):
    """Contrato para procesamiento de imágenes."""

    def load_from_url(self, image_url: str) -> Any:
        """Descarga y procesa una imagen remota para Tkinter."""
        ...

    def resize(self, image: Any, width: int, height: int) -> Any:
        """Redimensiona una imagen manteniendo proporción."""
        ...


@runtime_checkable
class IURLValidator(Protocol):
    """Contrato para validación de URLs."""

    def validate(self, url: str) -> Tuple[bool, Optional[str]]:
        """Valida una URL y retorna (es_valida, mensaje_error)."""
        ...


@runtime_checkable
class IThreadManager(Protocol):
    """Contrato para gestión de hilos."""

    def run(
        self,
        target: Callable,
        args: tuple = (),
        kwargs: Optional[dict] = None,
        daemon: bool = True,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_done: Optional[Callable[[], None]] = None,
        name: Optional[str] = None,
    ) -> Any:
        """Inicia un nuevo hilo."""
        ...

    def join_all(self, timeout: Optional[float] = None) -> None:
        ...

    def active_threads(self) -> Any:
        ...

    def errors(self) -> Any:
        ...


@runtime_checkable
class ITraceLogger(Protocol):
    """Contrato para logging estructurado."""

    def event(self, event: str, *, level: int = 20, **fields: Any) -> None:
        ...

    def warning(self, event: str, **fields: Any) -> None:
        ...

    def error(self, event: str, **fields: Any) -> None:
        ...

    def exception(self, event: str, **fields: Any) -> None:
        ...
