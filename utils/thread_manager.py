"""
Gestor de hilos para ejecuciones asíncronas sin bloquear la UI.
"""
import threading
from typing import Callable, List, Optional

from core.contracts import IThreadManager


class ThreadManager(IThreadManager):
    """Abstrae la creación y control de hilos secundarios."""

    def __init__(self):
        self._threads: List[threading.Thread] = []
        self._lock = threading.Lock()
        self._errors: List[Exception] = []

    def run(
        self,
        target: Callable,
        args: tuple = (),
        kwargs: Optional[dict] = None,
        daemon: bool = True,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_done: Optional[Callable[[], None]] = None,
        name: Optional[str] = None,
    ) -> threading.Thread:
        """Inicia un nuevo hilo con la función objetivo."""
        if kwargs is None:
            kwargs = {}

        def _runner() -> None:
            try:
                target(*args, **kwargs)
            except Exception as exc:
                with self._lock:
                    self._errors.append(exc)
                if on_error is not None:
                    on_error(exc)
                else:
                    raise
            else:
                if on_done is not None:
                    on_done()

        t = threading.Thread(target=_runner, daemon=daemon, name=name)
        with self._lock:
            self._threads.append(t)
        t.start()
        return t

    def join_all(self, timeout: Optional[float] = None) -> None:
        """Espera a que terminen todos los hilos registrados."""
        for thread in list(self._threads):
            thread.join(timeout)

    def active_threads(self) -> List[threading.Thread]:
        """Devuelve los hilos aún en ejecución."""
        return [thread for thread in self._threads if thread.is_alive()]

    def errors(self) -> List[Exception]:
        """Devuelve una copia de los errores capturados por hilos secundarios."""
        with self._lock:
            return list(self._errors)

    def clear_errors(self) -> None:
        """Limpia la lista de errores acumulados."""
        with self._lock:
            self._errors.clear()
