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
