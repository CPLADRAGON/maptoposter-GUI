"""Application entrypoint for the maptoposter PyQt6 GUI."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from .main_window import MainWindow
from .style import build_stylesheet


def main() -> int:
    """Launch the GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Map to Poster Studio")
    app.setStyleSheet(build_stylesheet())
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
