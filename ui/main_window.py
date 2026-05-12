"""
Layout principal de la ventana de Pecibalto.
"""
import tkinter as tk
from tkinter import ttk

from ui.components import StyledButton, URLInput, MutantButton


class MainWindow:
    """Ventana principal con la UI básica de entrada y búsqueda."""

    def __init__(self, root):
        self.root = root
        self.root.title("Pecibalto - Universal Media Extractor")
        self.root.geometry("700x400")
        self.root.configure(bg="#f5f6fa")
        self.root.minsize(500, 300)

        self.build_ui()

    def build_ui(self):
        """Construye los widgets principales."""
        # Contenedor central
        container = tk.Frame(self.root, bg="#f5f6fa")
        container.pack(expand=True, fill="both", padx=40, pady=40)

        # Título
        title = tk.Label(
            container,
            text="Pecibalto",
            font=("Helvetica", 28, "bold"),
            bg="#f5f6fa",
            fg="#2f3640"
        )
        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            container,
            text="Universal Media Extractor",
            font=("Helvetica", 12),
            bg="#f5f6fa",
            fg="#718093"
        )
        subtitle.pack(pady=(0, 40))

        # Marco de entrada
        input_frame = tk.Frame(container, bg="#f5f6fa")
        input_frame.pack(fill="x", pady=(0, 20))

        self.url_entry = URLInput(input_frame)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.url_entry.insert(0, "Pega aquí tu enlace...")
        self.url_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.url_entry.bind("<FocusOut>", self._on_entry_focus_out)

        self.find_button = MutantButton(
            input_frame,
            search_text="Encontrar",
            download_text="Descargar",
        )
        self.find_button.set_search_callback(self.handle_find)
        self.find_button.set_download_callback(self.handle_download)
        self.find_button.pack(side="right")

        # Barra de progreso (inicialmente oculta o en 0)
        self.progress = ttk.Progressbar(
            container,
            orient="horizontal",
            mode="determinate",
            length=100
        )
        self.progress.pack(fill="x", pady=(10, 0))
        self.progress["value"] = 0

    def _on_entry_focus_in(self, event):
        if self.url_entry.get() == "Pega aquí tu enlace...":
            self.url_entry.delete(0, "end")
            self.url_entry.config(fg="black")

    def _on_entry_focus_out(self, event):
        if not self.url_entry.get().strip():
            self.url_entry.insert(0, "Pega aquí tu enlace...")
            self.url_entry.config(fg="#999")

    def handle_find(self):
        """Acción temporal del botón Encontrar."""
        url = self.url_entry.get().strip()
        if url and url != "Pega aquí tu enlace...":
            print(f"[Pecibalto] Buscando: {url}")
        else:
            print("[Pecibalto] URL vacía")

    def handle_download(self):
        """Acción temporal del botón Descargar."""
        url = self.url_entry.get().strip()
        if url and url != "Pega aquí tu enlace...":
            print(f"[Pecibalto] Descargar: {url}")
        else:
            print("[Pecibalto] Descargar: URL vacía")
