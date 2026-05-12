"""
Gestor de hilos para ejecuciones asíncronas sin bloquear la UI.
"""
import threading


class ThreadManager:
    """Abstrae la creación y control de hilos secundarios."""

    def __init__(self):
        self._threads = []

    def run(self, target, args=(), kwargs=None, daemon=True):
        """Inicia un nuevo hilo con la función objetivo."""
        if kwargs is None:
            kwargs = {}
        t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=daemon)
        self._threads.append(t)
        t.start()
        return t
