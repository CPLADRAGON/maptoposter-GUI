"""Reusable PyQt6 widgets for the maptoposter GUI."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QDesktopServices, QPixmap
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QFrame,
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


class PosterPreview(QFrame):
    """Dark preview mat for generated poster outputs."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._pixmap: QPixmap | None = None
        self._output_path: Path | None = None
        self.setMinimumSize(420, 520)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(
            f"QFrame {{ background: {style.SURFACE_1}; border: 1px solid {style.BORDER}; border-radius: 18px; }}"
        )

        self.image = QLabel("Generated poster preview will appear here")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setObjectName("MutedLabel")
        self.image.setMinimumSize(320, 420)
        self.image.setStyleSheet(
            f"background: {style.SURFACE_2}; border: 1px solid {style.BORDER}; border-radius: 14px; padding: 16px;"
        )
        self.meta = QLabel("")
        self.meta.setObjectName("MutedLabel")
        self.meta.setWordWrap(True)
        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file)
        self.open_button.setEnabled(False)
        self.folder_button = QPushButton("Open Folder")
        self.folder_button.clicked.connect(self.open_folder)
        self.folder_button.setEnabled(False)

        actions = QHBoxLayout()
        actions.addWidget(self.open_button)
        actions.addWidget(self.folder_button)
        actions.addStretch(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.image, 1)
        layout.addWidget(self.meta)
        layout.addLayout(actions)

    def set_output(self, output_path: Path, output_format: str) -> None:
        """Show a generated output path, with inline preview for PNG files."""
        self._output_path = output_path
        self.open_button.setEnabled(True)
        self.folder_button.setEnabled(True)
        self.meta.setText(str(output_path))
        if output_format == "png" and output_path.exists():
            self._pixmap = QPixmap(str(output_path))
            self._update_scaled_pixmap()
        else:
            self._pixmap = None
            self.image.setPixmap(QPixmap())
            self.image.setText(f"{output_format.upper()} output saved. Use Open File to preview externally.")

    def resizeEvent(self, event) -> None:  # noqa: N802, ANN001
        super().resizeEvent(event)
        self._update_scaled_pixmap()

    def _update_scaled_pixmap(self) -> None:
        if self._pixmap is None or self._pixmap.isNull():
            return
        self.image.setText("")
        scaled = self._pixmap.scaled(
            self.image.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image.setPixmap(scaled)

    def open_file(self) -> None:
        if self._output_path is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._output_path.resolve())))

    def open_folder(self) -> None:
        if self._output_path is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self._output_path.parent.resolve())))
