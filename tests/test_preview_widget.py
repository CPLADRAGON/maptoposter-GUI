import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtGui import QImage  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

from maptoposter_gui.widgets import PosterPreview, ZoomableImageView  # noqa: E402


_APP = QApplication.instance() or QApplication(sys.argv)


def test_zoomable_image_view_exposes_zoom_and_reset_controls(tmp_path):
    image_path = tmp_path / "poster.png"
    image = QImage(20, 30, QImage.Format.Format_RGB32)
    image.fill(0x223344)
    assert image.save(str(image_path))

    view = ZoomableImageView()
    view.set_image(image_path)
    view.zoom_in()

    assert view.zoom_factor > 1.0

    view.reset_zoom()

    assert view.zoom_factor == 1.0


def test_poster_preview_displays_saved_file_location(tmp_path):
    image_path = tmp_path / "poster.png"
    image = QImage(20, 30, QImage.Format.Format_RGB32)
    image.fill(0x223344)
    assert image.save(str(image_path))

    preview = PosterPreview()
    preview.set_output(Path(image_path), "png")

    assert str(image_path) in preview.path_value.text()
    assert preview.copy_button.isEnabled()
    assert preview.open_button.isEnabled()
    assert preview.folder_button.isEnabled()
