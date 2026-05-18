"""Background generation worker for the PyQt6 GUI."""

from __future__ import annotations

import traceback

from PyQt6.QtCore import QObject, pyqtSignal

from maptoposter_core.generator import GenerationCancelled, MapPosterGenerator
from maptoposter_core.models import PosterRequest, ProgressEvent


class GenerationWorker(QObject):
    """Run poster generation off the UI thread."""

    progress = pyqtSignal(object)
    succeeded = pyqtSignal(object)
    failed = pyqtSignal(str, str)
    finished = pyqtSignal()

    def __init__(self, request: PosterRequest, generator: MapPosterGenerator | None = None) -> None:
        super().__init__()
        self.request = request
        self.generator = generator or MapPosterGenerator()
        self._cancelled = False

    def cancel(self) -> None:
        """Request cooperative cancellation at the next safe checkpoint."""
        self._cancelled = True

    def is_cancelled(self) -> bool:
        """Return whether cancellation has been requested."""
        return self._cancelled

    def run(self) -> None:
        """Generate the poster and emit Qt signals for the UI."""
        try:
            result = self.generator.generate(
                self.request,
                progress_callback=self._emit_progress,
                cancel_checker=self.is_cancelled,
            )
            self.succeeded.emit(result)
        except GenerationCancelled as exc:
            self.failed.emit(str(exc), "")
        except Exception as exc:  # noqa: BLE001 - GUI needs a user-facing failure path
            self.failed.emit(str(exc), traceback.format_exc())
        finally:
            self.finished.emit()

    def _emit_progress(self, event: ProgressEvent) -> None:
        self.progress.emit(event)
