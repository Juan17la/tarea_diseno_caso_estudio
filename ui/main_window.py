"""
Layout principal de la ventana de Pecibalto.
Vista pura: solo presentación, sin lógica de negocio.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Optional

import config as cfg
from ui.components import FormatSelector, MutantButton, URLInput


class MainWindow:
    """Ventana principal con la UI de entrada, preview y controles."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{cfg.APP_NAME} - {cfg.APP_SUBTITLE}")
        self.root.geometry(f"{cfg.WINDOW_WIDTH}x{cfg.WINDOW_HEIGHT}")
        self.root.configure(bg=cfg.BG_PRIMARY)
        self.root.minsize(cfg.WINDOW_MIN_WIDTH, cfg.WINDOW_MIN_HEIGHT)

        # Callbacks registrados por el controller
        self._on_find_clicked: Optional[Callable[[], None]] = None
        self._on_download_clicked: Optional[Callable[[], None]] = None
        self._on_format_changed: Optional[Callable[[str], None]] = None
        self._on_browse_clicked: Optional[Callable[[], None]] = None

        self.build_ui()

    def build_ui(self) -> None:
        """Construye los widgets principales."""
        container = tk.Frame(self.root, bg=cfg.BG_PRIMARY)
        container.pack(expand=True, fill="both", padx=40, pady=40)

        # Título
        tk.Label(
            container,
            text=cfg.APP_NAME,
            font=cfg.FONT_TITLE,
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_PRIMARY,
        ).pack(pady=(0, 5))

        tk.Label(
            container,
            text=cfg.APP_SUBTITLE,
            font=cfg.FONT_SUBTITLE,
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_SECONDARY,
        ).pack(pady=(0, 40))

        # Input + Botón
        input_frame = tk.Frame(container, bg=cfg.BG_PRIMARY)
        input_frame.pack(fill="x", pady=(0, 20))

        self.url_entry = URLInput(input_frame)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.url_entry.insert(0, cfg.URL_PLACEHOLDER)
        self.url_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.url_entry.bind("<FocusOut>", self._on_entry_focus_out)

        self.find_button = MutantButton(
            input_frame,
            search_text="Encontrar",
            download_text="Descargar",
        )
        self.find_button.pack(side="right")

        # Selector de formato
        self.format_selector = FormatSelector(container)
        self.format_selector.pack(fill="x", pady=(0, 10))
        self.format_selector.set_on_change(self._trigger_format_changed)

        # Ruta destino
        path_frame = tk.Frame(container, bg=cfg.BG_PRIMARY)
        path_frame.pack(fill="x", pady=(0, 10))

        self.path_label = tk.Label(
            path_frame,
            text="Destino: (predeterminado)",
            font=(cfg.FONT_FAMILY, 10),
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_SECONDARY,
            anchor="w",
        )
        self.path_label.pack(side="left", fill="x", expand=True)

        browse_btn = tk.Button(
            path_frame,
            text="📁",
            command=self._trigger_browse,
            bg=cfg.BG_PRIMARY,
            relief="flat",
            cursor="hand2",
        )
        browse_btn.pack(side="right")

        # Preview area (miniatura + título)
        self.preview_frame = tk.Frame(container, bg=cfg.BG_PRIMARY)
        self.preview_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.thumbnail_label = tk.Label(
            self.preview_frame,
            bg=cfg.BG_PRIMARY,
        )
        self.thumbnail_label.pack(pady=(0, 5))

        self.title_label = tk.Label(
            self.preview_frame,
            text="",
            font=(cfg.FONT_FAMILY, 11, "bold"),
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_PRIMARY,
            wraplength=cfg.WINDOW_WIDTH - 100,
        )
        self.title_label.pack()

        # Barra de progreso
        self.progress = ttk.Progressbar(
            container,
            orient="horizontal",
            mode="determinate",
        )
        self.progress.pack(fill="x", pady=(10, 0))
        self.progress["value"] = 0

    # ---- Registro de callbacks ----

    def set_on_find_clicked(self, callback: Callable[[], None]) -> None:
        self._on_find_clicked = callback
        self.find_button.set_search_callback(self._trigger_find)

    def set_on_download_clicked(self, callback: Callable[[], None]) -> None:
        self._on_download_clicked = callback
        self.find_button.set_download_callback(self._trigger_download)

    def set_on_format_changed(self, callback: Callable[[str], None]) -> None:
        self._on_format_changed = callback

    def set_on_browse_clicked(self, callback: Callable[[], None]) -> None:
        self._on_browse_clicked = callback

    # ---- Triggers internos ----

    def _trigger_find(self):
        if self._on_find_clicked is not None:
            self._on_find_clicked()

    def _trigger_download(self):
        if self._on_download_clicked is not None:
            self._on_download_clicked()

    def _trigger_format_changed(self, value: str):
        if self._on_format_changed is not None:
            self._on_format_changed(value)

    def _trigger_browse(self):
        if self._on_browse_clicked is not None:
            self._on_browse_clicked()

    def _on_entry_focus_in(self, event=None):
        if self.url_entry.get() == cfg.URL_PLACEHOLDER:
            self.url_entry.delete(0, "end")
            self.url_entry.config(fg="black")

    def _on_entry_focus_out(self, event=None):
        if not self.url_entry.get().strip():
            self.url_entry.insert(0, cfg.URL_PLACEHOLDER)
            self.url_entry.config(fg=cfg.PLACEHOLDER_FG)

    # ---- Métodos de presentación ----

    def get_url(self) -> str:
        url = self.url_entry.get().strip()
        return "" if url == cfg.URL_PLACEHOLDER else url

    def set_thumbnail(self, image_tk) -> None:
        self.thumbnail_label.config(image=image_tk)
        self.thumbnail_label.image = image_tk  # keep reference

    def set_title(self, text: str) -> None:
        self.title_label.config(text=text)

    def set_progress(self, value: float) -> None:
        self.progress["value"] = max(0.0, min(100.0, value))

    def reset_progress(self) -> None:
        self.progress["value"] = 0

    def set_destination_path(self, path: str) -> None:
        display = path if path else "(predeterminado)"
        self.path_label.config(text=f"Destino: {display}")

    def get_selected_format(self) -> str:
        return self.format_selector.get_selected()

    def show_warning(self, title: str, message: str) -> None:
        messagebox.showwarning(title, message)

    def show_info(self, title: str, message: str) -> None:
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message)

    def get_destination_path(self) -> str:
        text = self.path_label.cget("text")
        if text == "Destino: (predeterminado)":
            return ""
        return text.replace("Destino: ", "", 1)

    def reset(self) -> None:
        """Limpia la interfaz para una nueva búsqueda."""
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, cfg.URL_PLACEHOLDER)
        self.url_entry.config(fg=cfg.PLACEHOLDER_FG)
        self.find_button.to_search()
        self.thumbnail_label.config(image="")
        self.thumbnail_label.image = None
        self.title_label.config(text="")
        self.reset_progress()
        self.set_destination_path("")
