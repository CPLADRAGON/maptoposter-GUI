"""Shared request, result, and progress models for poster generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_FORMATS = {"png", "svg", "pdf"}


@dataclass(slots=True)
class PosterRequest:
    """Inputs required to generate a map poster."""

    city: str
    country: str
    theme: str = "terracotta"
    distance: int = 18000
    width: float = 12.0
    height: float = 16.0
    output_format: str = "png"
    latitude: str | None = None
    longitude: str | None = None
    country_label: str | None = None
    display_city: str | None = None
    display_country: str | None = None
    font_family: str | None = None

    def validate(self) -> None:
        """Validate fields and raise ValueError with a user-facing message."""
        if not self.city.strip():
            raise ValueError("City is required.")
        if not self.country.strip():
            raise ValueError("Country is required.")
        if bool(self.latitude) != bool(self.longitude):
            raise ValueError("Latitude and longitude must be provided together.")
        if self.distance <= 0:
            raise ValueError("Distance must be greater than zero.")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be greater than zero.")
        if self.width > 20 or self.height > 20:
            raise ValueError("Width and height must be 20 inches or less.")
        if self.output_format.lower() not in SUPPORTED_FORMATS:
            formats = ", ".join(sorted(SUPPORTED_FORMATS))
            raise ValueError(f"Output format must be one of: {formats}.")


@dataclass(slots=True)
class PosterResult:
    """Result produced by a successful poster generation run."""

    output_path: Path
    theme: str
    coordinates: tuple[float, float]
    output_format: str
    elapsed_seconds: float


@dataclass(slots=True)
class ProgressEvent:
    """Progress update emitted by generation services and consumed by the GUI."""

    phase: str
    message: str
    current: int = 0
    total: int = 0
    percent: int | None = None
