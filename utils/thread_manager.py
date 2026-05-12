"""
Gestor de hilos para ejecuciones asíncronas sin bloquear la UI.
"""

import threading
from typing import Callable, Optional


class ThreadManager:
    """Abstrae la creación y control de hilos secundarios."""

    def __init__(self):
        self._threads = []
        self._lock = threading.Lock()
        self._errors = []

    def run(
        self,
        target,
        args=(),
        kwargs=None,
        daemon=True,
        on_error: Optional[Callable[[Exception], None]] = None,
        name: Optional[str] = None,
    ):
        """Inicia un nuevo hilo con la función objetivo."""
        if kwargs is None:
            kwargs = {}

        def _runner():
            try:
                target(*args, **kwargs)
            except Exception as exc:
                with self._lock:
                    self._errors.append(exc)
                if on_error:
                    on_error(exc)
                else:
                    raise

        t = threading.Thread(target=_runner, daemon=daemon, name=name)
        self._threads.append(t)
        t.start()
        return t

    def join_all(self, timeout=None):
        """Espera a que terminen todos los hilos registrados."""
        for thread in list(self._threads):
            thread.join(timeout)

    def active_threads(self):
        """Devuelve los hilos aún en ejecución."""
        return [thread for thread in self._threads if thread.is_alive()]

    def errors(self):
        """Devuelve una copia de los errores capturados por hilos secundarios."""
        with self._lock:
            return list(self._errors)
