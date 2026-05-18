"""Reusable PyQt6 widgets for the maptoposter GUI."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QColor, QDesktopServices, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from maptoposter_core.themes import ThemeMetadata

from . import style


class ColorSwatch(QFrame):
    """Small color chip for theme previews."""

    def __init__(self, label: str, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(42, 32)
        self.setToolTip(f"{label}: {color}")
        QColor(color)  # validates common Qt color strings without raising for named colors
        self.setStyleSheet(
            f"background: {color}; border: 1px solid {style.BORDER}; border-radius: 8px;"
        )


class ThemeSwatchCard(QFrame):
    """Theme metadata and color swatches."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            f"QFrame {{ background: {style.SURFACE_1}; border: 1px solid {style.BORDER}; border-radius: 16px; }}"
        )
        self.title = QLabel("Theme")
        self.title.setObjectName("HeroTitle")
        self.description = QLabel("Select a theme to preview its palette.")
        self.description.setWordWrap(True)
        self.description.setObjectName("MutedLabel")
        self.swatch_row = QHBoxLayout()
        self.swatch_row.setSpacing(8)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addLayout(self.swatch_row)

    def update_theme(self, metadata: ThemeMetadata) -> None:
        """Update visible theme metadata and color chips."""
        self.title.setText(metadata.name)
        self.description.setText(metadata.description)
        while self.swatch_row.count():
            item = self.swatch_row.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        keys = [
            "bg",
            "text",
            "water",
            "parks",
            "road_motorway",
            "road_primary",
            "road_secondary",
            "road_tertiary",
            "road_residential",
        ]
        for key in keys:
            color = metadata.colors.get(key)
            if color:
                self.swatch_row.addWidget(ColorSwatch(key, color))
        self.swatch_row.addStretch(1)


class ZoomableImageView(QGraphicsView):
    """Graphics view that supports wheel zoom, drag-to-pan, and reset."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.zoom_factor = 1.0
        self._scene = QGraphicsScene(self)
        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self._message_item = self._scene.addText("")
        self._message_item.setDefaultTextColor(QColor(style.TEXT_MUTED))
        self.setScene(self._scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(
            f"background: {style.SURFACE_2}; border: 1px solid {style.BORDER}; border-radius: 14px;"
        )

    def set_image(self, image_path: Path) -> None:
        """Load an image and fit it into the available viewport."""
        pixmap = QPixmap(str(image_path))
        self._pixmap_item.setPixmap(pixmap)
        self._message_item.setPlainText("")
        self._scene.setSceneRect(self._pixmap_item.boundingRect())
        self.reset_zoom()

    def clear_image(self, message: str) -> None:
        """Clear the image and show a text-only scene message."""
        self._pixmap_item.setPixmap(QPixmap())
        self._message_item.setPlainText(message)
        self._scene.setSceneRect(self._message_item.boundingRect())
        self.resetTransform()
        self.zoom_factor = 1.0

    def zoom_in(self) -> None:
        """Zoom in around the current view center."""
        self._apply_zoom(1.25)

    def zoom_out(self) -> None:
        """Zoom out around the current view center."""
        self._apply_zoom(0.8)

    def reset_zoom(self) -> None:
        """Fit the image/scene into the viewport and reset zoom state."""
        self.resetTransform()
        self.zoom_factor = 1.0
        if not self._scene.sceneRect().isEmpty():
            self.fitInView(self._scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event) -> None:  # noqa: N802, ANN001
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def _apply_zoom(self, factor: float) -> None:
        new_zoom = self.zoom_factor * factor
        if new_zoom < 0.2 or new_zoom > 8.0:
            return
        self.zoom_factor = new_zoom
        self.scale(factor, factor)


class PosterPreview(QFrame):
    """Dark preview mat for generated poster outputs."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._output_path: Path | None = None
        self.setMinimumSize(360, 420)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(
            f"QFrame {{ background: {style.SURFACE_1}; border: 1px solid {style.BORDER}; border-radius: 18px; }}"
        )

        self.image = ZoomableImageView()
        self.image.clear_image("Generated poster preview will appear here")
        self.help_label = QLabel("Scroll to zoom. Drag the poster to pan when zoomed.")
        self.help_label.setObjectName("MutedLabel")
        self.meta = QLabel("")
        self.meta.setObjectName("MutedLabel")
        self.meta.setWordWrap(True)
        self.path_label = QLabel("Saved file:")
        self.path_label.setObjectName("MutedLabel")
        self.path_value = QLabel("Not generated yet")
        self.path_value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.path_value.setWordWrap(True)
        self.path_value.setObjectName("MutedLabel")

        self.zoom_out_button = QPushButton("−")
        self.zoom_out_button.setToolTip("Zoom out")
        self.zoom_out_button.clicked.connect(self.image.zoom_out)
        self.reset_zoom_button = QPushButton("Fit")
        self.reset_zoom_button.setToolTip("Fit preview")
        self.reset_zoom_button.clicked.connect(self.image.reset_zoom)
        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.setToolTip("Zoom in")
        self.zoom_in_button.clicked.connect(self.image.zoom_in)
        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file)
        self.open_button.setEnabled(False)
        self.folder_button = QPushButton("Open Folder")
        self.folder_button.clicked.connect(self.open_folder)
        self.folder_button.setEnabled(False)
        self.copy_button = QPushButton("Copy Path")
        self.copy_button.clicked.connect(self.copy_path)
        self.copy_button.setEnabled(False)

        zoom_actions = QHBoxLayout()
        zoom_actions.addWidget(self.zoom_out_button)
        zoom_actions.addWidget(self.reset_zoom_button)
        zoom_actions.addWidget(self.zoom_in_button)
        zoom_actions.addStretch(1)

        actions = QHBoxLayout()
        actions.addWidget(self.open_button)
        actions.addWidget(self.folder_button)
        actions.addWidget(self.copy_button)
        actions.addStretch(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.image, 1)
        layout.addWidget(self.help_label)
        layout.addLayout(zoom_actions)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_value)
        layout.addWidget(self.meta)
        layout.addLayout(actions)

    def set_output(self, output_path: Path, output_format: str) -> None:
        """Show a generated output path, with inline preview for PNG files."""
        self._output_path = output_path
        self.open_button.setEnabled(True)
        self.folder_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        resolved = output_path.resolve()
        self.path_value.setText(str(resolved))
        self.meta.setText(f"Format: {output_format.upper()}")
        if output_format == "png" and output_path.exists():
            self.image.set_image(output_path)
        else:
            self.image.clear_image(f"{output_format.upper()} output saved. Use Open File to preview externally.")

    def open_file(self) -> None:
        if self._output_path is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._output_path.resolve())))

    def open_folder(self) -> None:
        if self._output_path is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._output_path.parent.resolve())))

    def copy_path(self) -> None:
        if self._output_path is not None:
            QApplication.clipboard().setText(str(self._output_path.resolve()))
