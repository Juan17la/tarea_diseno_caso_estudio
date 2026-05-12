"""
Punto de entrada principal de Pecibalto.
"""
import os
import sys


def _configure_tcltk_environment() -> None:
    """Configura variables de entorno Tcl/Tk si no están definidas."""
    if "TCL_LIBRARY" in os.environ and "TK_LIBRARY" in os.environ:
        return

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
        tk_c = c.replace("tcl8.", "tk8.")
        if os.path.isdir(tk_c) and "TK_LIBRARY" not in os.environ:
            os.environ["TK_LIBRARY"] = tk_c


if __name__ == "__main__":
    _configure_tcltk_environment()

    import tkinter as tk

    from controller import AppController
    from services.extractor_service import ExtractorService
    from services.image_service import ImageService
    from traceability import get_trace_logger
    from ui.main_window import MainWindow
    from utils.thread_manager import ThreadManager
    from utils.validator import URLValidator

    root = tk.Tk()
    view = MainWindow(root)

    controller = AppController(
        view=view,
        extractor=ExtractorService(),
        image_service=ImageService(),
        thread_manager=ThreadManager(),
        validator=URLValidator(),
        logger=get_trace_logger(),
    )

    root.mainloop()
