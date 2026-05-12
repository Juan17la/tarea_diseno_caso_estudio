"""
Widgets personalizados reutilizables para la interfaz de Pecibalto.
"""
import tkinter as tk


class URLInput(tk.Entry):
    """Campo de entrada estilizado para URLs."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=("Helvetica", 11),
            relief="solid",
            bd=1,
            highlightbackground="#ccc",
            highlightcolor="#007bff",
            highlightthickness=1,
            **kwargs
        )


class StyledButton(tk.Button):
    """Botón estilizado con colores planos."""

    def __init__(self, parent, text="Botón", command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=("Helvetica", 10, "bold"),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            command=command,
            cursor="hand2",
            **kwargs
        )


class MutantButton(StyledButton):
    """Botón que alterna visual y comportamiento entre 'buscar' y 'descargar'.

    - Estado inicial: 'search' (texto configurable).
    - Al pulsar en 'search' llama al callback de búsqueda (si está) y pasa
      al estado 'download'.
    - Al pulsar en 'download' llama al callback de descarga (si está).
    """

    def __init__(self, parent, search_text="Encontrar", download_text="Descargar", **kwargs):
        super().__init__(parent, text=search_text, **kwargs)
        self._search_text = search_text
        self._download_text = download_text
        self._state = "search"
        self._search_callback = None
        self._download_callback = None
        self._normal_bg = self.cget("bg")
        self._hover_bg = "#0069d9"
        self.config(command=self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event=None):
        self.configure(bg=self._hover_bg)

    def _on_leave(self, _event=None):
        self.configure(bg=self._normal_bg)

    def set_search_callback(self, cb):
        self._search_callback = cb

    def set_download_callback(self, cb):
        self._download_callback = cb

    def _on_click(self):
        if self._state == "search":
            if callable(self._search_callback):
                try:
                    self._search_callback()
                except Exception:
                    pass
            self.to_download()
        else:
            if callable(self._download_callback):
                try:
                    self._download_callback()
                except Exception:
                    pass

    def to_search(self):
        self.config(text=self._search_text)
        self._state = "search"

    def to_download(self):
        self.config(text=self._download_text)
        self._state = "download"
