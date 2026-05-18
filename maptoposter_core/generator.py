"""High-level poster generation API shared by CLI-compatible code and GUI."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from lat_lon_parser import parse

import create_map_poster as legacy
from font_management import load_fonts

from .models import PosterRequest, PosterResult, ProgressEvent
from .themes import ThemeManager

ProgressCallback = Callable[[ProgressEvent], None]
CancelChecker = Callable[[], bool]


class GenerationCancelled(RuntimeError):
    """Raised when a poster generation request is cancelled at a safe checkpoint."""


class MapPosterGenerator:
    """Generate posters through a reusable API while preserving legacy rendering."""

    def __init__(self, theme_manager: ThemeManager | None = None) -> None:
        self.theme_manager = theme_manager or ThemeManager()

    def generate(
        self,
        request: PosterRequest,
        progress_callback: ProgressCallback | None = None,
        cancel_checker: CancelChecker | None = None,
    ) -> PosterResult:
        """Generate a poster and return output metadata."""
        start = time.monotonic()
        request.validate()
        output_format = request.output_format.lower()

        self._emit(progress_callback, "validate", "Validated poster settings", 1, 6)
        self._raise_if_cancelled(cancel_checker)

        self._emit(progress_callback, "theme", f"Loading theme: {request.theme}", 2, 6)
        theme = self.theme_manager.load_theme(request.theme)
        legacy.THEME = theme
        self._raise_if_cancelled(cancel_checker)

        custom_fonts = None
        if request.font_family:
            self._emit(progress_callback, "fonts", f"Loading font: {request.font_family}", 3, 6)
            custom_fonts = load_fonts(request.font_family)
        else:
            self._emit(progress_callback, "fonts", "Using bundled Roboto fonts", 3, 6)
        self._raise_if_cancelled(cancel_checker)

        if request.latitude and request.longitude:
            coordinates = (parse(request.latitude), parse(request.longitude))
            self._emit(progress_callback, "coordinates", "Using custom coordinates", 4, 6)
        else:
            self._emit(progress_callback, "coordinates", "Looking up coordinates", 4, 6)
            coordinates = legacy.get_coordinates(request.city, request.country)
        self._raise_if_cancelled(cancel_checker)

        if request.distance >= 15000:
            download_message = "Downloading a large street network. This blocking OpenStreetMap request can take several minutes."
        else:
            download_message = "Downloading street network, water, and parks. The first OpenStreetMap request may pause here."
        self._emit(progress_callback, "render", download_message, 5, 6)
        output_file = legacy.generate_output_filename(request.city, request.theme, output_format)
        legacy.create_poster(
            request.city,
            request.country,
            coordinates,
            request.distance,
            output_file,
            output_format,
            request.width,
            request.height,
            country_label=request.country_label,
            display_city=request.display_city,
            display_country=request.display_country,
            fonts=custom_fonts,
        )
        self._raise_if_cancelled(cancel_checker)

        elapsed = time.monotonic() - start
        self._emit(progress_callback, "saved", f"Saved poster to {output_file}", 6, 6)
        return PosterResult(
            output_path=Path(output_file),
            theme=request.theme,
            coordinates=coordinates,
            output_format=output_format,
            elapsed_seconds=elapsed,
        )

    @staticmethod
    def _emit(
        progress_callback: ProgressCallback | None,
        phase: str,
        message: str,
        current: int,
        total: int,
    ) -> None:
        if progress_callback is None:
            return
        percent = int((current / total) * 100) if total else None
        progress_callback(ProgressEvent(phase, message, current, total, percent))

    @staticmethod
    def _raise_if_cancelled(cancel_checker: CancelChecker | None) -> None:
        if cancel_checker is not None and cancel_checker():
            raise GenerationCancelled("Poster generation was cancelled.")
