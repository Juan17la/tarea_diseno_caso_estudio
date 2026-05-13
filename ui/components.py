"""
Widgets personalizados reutilizables para la interfaz de Pecibalto.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

import config as cfg


class URLInput(tk.Entry):
    """Campo de entrada estilizado para URLs."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=cfg.FONT_INPUT,
            relief="solid",
            bd=1,
            highlightbackground=cfg.BORDER,
            highlightcolor=cfg.ACCENT,
            highlightthickness=1,
            **kwargs,
        )


class StyledButton(tk.Button):
    """Botón estilizado con colores planos."""

    def __init__(self, parent, text="Botón", command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=cfg.FONT_BUTTON,
            bg=cfg.ACCENT,
            fg="white",
            activebackground=cfg.ACCENT_ACTIVE,
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            command=command,
            cursor="hand2",
            **kwargs,
        )


class MutantButton(StyledButton):
    """Botón que alterna visual y comportamiento entre 'buscar' y 'descargar'."""

    _DOWNLOAD_BG = "#28a745"
    _DOWNLOAD_HOVER = "#218838"

    def __init__(
        self,
        parent,
        search_text="Encontrar",
        download_text="Descargar",
        **kwargs,
    ):
        super().__init__(parent, text=search_text, **kwargs)
        self._search_text = search_text
        self._download_text = download_text
        self._state = "search"
        self._search_callback: Optional[Callable[[], None]] = None
        self._download_callback: Optional[Callable[[], None]] = None
        self._normal_bg = cfg.ACCENT
        self._hover_bg = cfg.ACCENT_HOVER
        self.config(command=self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event=None):
        if str(self.cget("state")) != "disabled":
            self.configure(bg=self._hover_bg)

    def _on_leave(self, _event=None):
        if str(self.cget("state")) != "disabled":
            self.configure(bg=self._normal_bg)

    def set_search_callback(self, cb: Optional[Callable[[], None]]) -> None:
        self._search_callback = cb

    def set_download_callback(self, cb: Optional[Callable[[], None]]) -> None:
        self._download_callback = cb

    def set_enabled(self, enabled: bool) -> None:
        self.config(state="normal" if enabled else "disabled")

    def _on_click(self):
        if self._state == "search":
            self.set_enabled(False)
            if self._search_callback is not None:
                self._search_callback()
            self.to_download()
        elif self._state == "download":
            self.set_enabled(False)
            if self._download_callback is not None:
                self._download_callback()

    def to_search(self):
        self._state = "search"
        self._normal_bg = cfg.ACCENT
        self._hover_bg = cfg.ACCENT_HOVER
        self.config(text=self._search_text, bg=cfg.ACCENT, state="normal")

    def to_download(self):
        self._state = "download"
        self._normal_bg = self._DOWNLOAD_BG
        self._hover_bg = self._DOWNLOAD_HOVER
        self.config(text=self._download_text, bg=self._DOWNLOAD_BG)


class FormatSelector(tk.Frame):
    """Selector de perfil de formato (Combobox)."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=cfg.BG_PRIMARY, **kwargs)
        self._on_change: Optional[Callable[[str], None]] = None

        tk.Label(
            self,
            text="Formato:",
            font=(cfg.FONT_FAMILY, 10),
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_PRIMARY,
        ).pack(side="left", padx=(0, 10))

        self._combo = ttk.Combobox(
            self,
            values=list(cfg.FORMAT_PROFILES.keys()),
            state="readonly",
            font=(cfg.FONT_FAMILY, 10),
        )
        self._combo.set(cfg.DEFAULT_FORMAT)
        self._combo.pack(side="left", fill="x", expand=True)
        self._combo.bind("<<ComboboxSelected>>", self._on_combo_changed)

    def set_on_change(self, callback: Callable[[str], None]) -> None:
        self._on_change = callback

    def _on_combo_changed(self, event=None):
        if self._on_change is not None:
            self._on_change(self._combo.get())

    def get_selected(self) -> str:
        return self._combo.get()

    def get_selected_profile(self) -> dict:
        return cfg.FORMAT_PROFILES[self.get_selected()]

    def reset(self) -> None:
        self._combo.set(cfg.DEFAULT_FORMAT)
