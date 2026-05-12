"""
Punto de entrada principal de Pecibalto.

Se intenta corregir problemas de instalación de Tcl/Tk configurando
variables de entorno `TCL_LIBRARY` y `TK_LIBRARY` a rutas típicas
de la instalación de Python antes de inicializar `tkinter`.
"""
import os
import sys

# Intento mínimo y seguro de localizar las carpetas de Tcl/Tk dentro
# de la instalación de Python para evitar el error "Can't find a usable init.tcl".
if "TCL_LIBRARY" not in os.environ or "TK_LIBRARY" not in os.environ:
    base = getattr(sys, "base_prefix", sys.prefix)
    candidates = [
        os.path.join(base, "tcl", "tcl8.6"),
        os.path.join(base, "tcl", "tcl8.5"),
        os.path.join(base, "lib", "tcl8.6"),
        os.path.join(base, "lib", "tcl8.5"),
    ]
    for c in candidates:
        if os.path.isdir(c) and "TCL_LIBRARY" not in os.environ:
            os.environ["TCL_LIBRARY"] = c
        # tk library often sits alongside tcl under the 'tcl' folder
        tk_c = c.replace("tcl8.", "tk8.")
        if os.path.isdir(tk_c) and "TK_LIBRARY" not in os.environ:
            os.environ["TK_LIBRARY"] = tk_c

import tkinter as tk
from ui.main_window import MainWindow


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
