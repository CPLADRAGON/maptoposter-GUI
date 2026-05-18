"""Main PyQt6 window for maptoposter."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QThread, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from maptoposter_core.models import PosterRequest, PosterResult, ProgressEvent
from maptoposter_core.themes import ThemeManager

from .widgets import PosterPreview, ThemeSwatchCard
from .worker import GenerationWorker


class MainWindow(QMainWindow):
    """Dark-mode-first desktop interface for generating map posters."""

    def __init__(self) -> None:
        super().__init__()
        self.theme_manager = ThemeManager()
        self.worker: GenerationWorker | None = None
        self.worker_thread: QThread | None = None

        self.setWindowTitle("Map to Poster Studio")
        self.resize(1180, 760)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Paris")
        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("France")
        self.latitude_input = QLineEdit()
        self.latitude_input.setPlaceholderText("Optional")
        self.longitude_input = QLineEdit()
        self.longitude_input.setPlaceholderText("Optional")
        self.display_city_input = QLineEdit()
        self.display_country_input = QLineEdit()
        self.country_label_input = QLineEdit()
        self.font_family_input = QLineEdit()
        self.font_family_input.setPlaceholderText("Optional Google Font family")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.list_theme_names())
        index = self.theme_combo.findText("terracotta")
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        self.theme_combo.currentTextChanged.connect(self.update_theme_preview)

        self.distance_input = QSpinBox()
        self.distance_input.setRange(1, 100000)
        self.distance_input.setValue(18000)
        self.distance_input.setSuffix(" m")

        self.width_input = QDoubleSpinBox()
        self.width_input.setRange(0.1, 20.0)
        self.width_input.setDecimals(1)
        self.width_input.setValue(12.0)
        self.width_input.setSuffix(" in")
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(0.1, 20.0)
        self.height_input.setDecimals(1)
        self.height_input.setValue(16.0)
        self.height_input.setSuffix(" in")

        self.format_combo = QComboBox()
        self.format_combo.addItems(["png", "svg", "pdf"])

        self.appearance_combo = QComboBox()
        self.appearance_combo.addItems(["Dark"])
        self.appearance_combo.setToolTip("Dark mode is implemented first; system/light modes can be added later.")

        self.generate_button = QPushButton("Generate Poster")
        self.generate_button.setObjectName("PrimaryButton")
        self.generate_button.clicked.connect(self.start_generation)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("DangerButton")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_generation)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.status_label = QLabel("Ready to generate a poster.")
        self.status_label.setObjectName("MutedLabel")

        self.theme_preview = ThemeSwatchCard()
        self.poster_preview = PosterPreview()

        self.setCentralWidget(self._build_layout())
        self.update_theme_preview(self.theme_combo.currentText())

    def _build_layout(self) -> QWidget:
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(14)

        hero = QLabel("Map to Poster Studio")
        hero.setObjectName("HeroTitle")
        subtitle = QLabel("Generate minimalist city map posters from OpenStreetMap data.")
        subtitle.setObjectName("MutedLabel")
        outer.addWidget(hero)
        outer.addWidget(subtitle)

        body = QHBoxLayout()
        body.setSpacing(16)
        body.addWidget(self._build_controls(), 0)

        preview_stack = QVBoxLayout()
        preview_stack.setSpacing(14)
        preview_stack.addWidget(self.theme_preview, 0)
        preview_stack.addWidget(self.poster_preview, 1)
        preview_holder = QWidget()
        preview_holder.setLayout(preview_stack)
        body.addWidget(preview_holder, 1)
        outer.addLayout(body, 1)

        footer = QHBoxLayout()
        footer.addWidget(self.status_label, 1)
        footer.addWidget(self.progress, 1)
        footer.addWidget(self.cancel_button)
        footer.addWidget(self.generate_button)
        outer.addLayout(footer)
        return root

    def _build_controls(self) -> QScrollArea:
        panel = QWidget()
        panel.setFixedWidth(390)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(self._group("Location", [
            ("City", self.city_input),
            ("Country", self.country_input),
            ("Latitude", self.latitude_input),
            ("Longitude", self.longitude_input),
        ]))
        layout.addWidget(self._group("Poster Settings", [
            ("Theme", self.theme_combo),
            ("Distance", self.distance_input),
            ("Width", self.width_input),
            ("Height", self.height_input),
            ("Format", self.format_combo),
        ]))
        layout.addWidget(self._group("Typography", [
            ("Display city", self.display_city_input),
            ("Display country", self.display_country_input),
            ("Country label", self.country_label_input),
            ("Font family", self.font_family_input),
        ]))
        layout.addWidget(self._group("Appearance", [("Mode", self.appearance_combo)]))
        layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidget(panel)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFixedWidth(410)
        return scroll

    @staticmethod
    def _group(title: str, rows: list[tuple[str, QWidget]]) -> QGroupBox:
        group = QGroupBox(title)
        form = QFormLayout(group)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)
        for label, widget in rows:
            form.addRow(label, widget)
        return group

    def update_theme_preview(self, theme_name: str) -> None:
        if not theme_name:
            return
        try:
            self.theme_preview.update_theme(self.theme_manager.get_metadata(theme_name))
        except Exception as exc:  # noqa: BLE001
            self.status_label.setText(f"Theme preview failed: {exc}")

    def build_request(self) -> PosterRequest:
        return PosterRequest(
            city=self.city_input.text().strip(),
            country=self.country_input.text().strip(),
            latitude=self.latitude_input.text().strip() or None,
            longitude=self.longitude_input.text().strip() or None,
            country_label=self.country_label_input.text().strip() or None,
            theme=self.theme_combo.currentText(),
            distance=self.distance_input.value(),
            width=self.width_input.value(),
            height=self.height_input.value(),
            output_format=self.format_combo.currentText(),
            display_city=self.display_city_input.text().strip() or None,
            display_country=self.display_country_input.text().strip() or None,
            font_family=self.font_family_input.text().strip() or None,
        )

    def start_generation(self) -> None:
        try:
            request = self.build_request()
            request.validate()
        except ValueError as exc:
            self.status_label.setText(str(exc))
            QMessageBox.warning(self, "Check poster settings", str(exc))
            return

        self.set_busy(True)
        self.progress.setValue(0)
        self.status_label.setText("Starting generation…")
        self.worker_thread = QThread(self)
        self.worker = GenerationWorker(request)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.on_progress)
        self.worker.succeeded.connect(self.on_success)
        self.worker.failed.connect(self.on_failure)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.on_thread_finished)
        self.worker_thread.start()

    def cancel_generation(self) -> None:
        if self.worker is not None:
            self.worker.cancel()
            self.status_label.setText("Cancellation requested. Waiting for the current safe checkpoint…")

    def on_progress(self, event: ProgressEvent) -> None:
        self.status_label.setText(event.message)
        if event.percent is not None:
            self.progress.setValue(event.percent)

    def on_success(self, result: PosterResult) -> None:
        self.progress.setValue(100)
        self.status_label.setText(f"Saved poster in {result.elapsed_seconds:.1f}s")
        self.poster_preview.set_output(Path(result.output_path), result.output_format)

    def on_failure(self, message: str, details: str) -> None:
        self.status_label.setText(message)
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle("Generation failed")
        box.setText(message)
        if details:
            box.setDetailedText(details)
        box.exec()

    def on_thread_finished(self) -> None:
        self.worker = None
        self.worker_thread = None
        self.set_busy(False)

    def set_busy(self, busy: bool) -> None:
        self.generate_button.setEnabled(not busy)
        self.cancel_button.setEnabled(busy)
        for widget in [
            self.city_input,
            self.country_input,
            self.latitude_input,
            self.longitude_input,
            self.display_city_input,
            self.display_country_input,
            self.country_label_input,
            self.font_family_input,
            self.theme_combo,
            self.distance_input,
            self.width_input,
            self.height_input,
            self.format_combo,
        ]:
            widget.setEnabled(not busy)
