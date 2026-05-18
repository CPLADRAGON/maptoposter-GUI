"""Theme discovery and metadata helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

FILE_ENCODING = "utf-8"


@dataclass(frozen=True, slots=True)
class ThemeMetadata:
    """Theme information needed by GUI selectors and swatches."""

    identifier: str
    name: str
    description: str
    colors: dict[str, str]


class ThemeManager:
    """Load and describe JSON themes without changing their on-disk schema."""

    def __init__(self, themes_dir: str | Path = "themes") -> None:
        self.themes_dir = Path(themes_dir)

    def list_theme_names(self) -> list[str]:
        """Return sorted theme identifiers from the themes directory."""
        if not self.themes_dir.exists():
            return []
        return sorted(path.stem for path in self.themes_dir.glob("*.json"))

    def load_theme(self, theme_name: str = "terracotta") -> dict[str, Any]:
        """Load a theme by identifier."""
        theme_path = self.themes_dir / f"{theme_name}.json"
        if not theme_path.exists():
            raise FileNotFoundError(f"Theme '{theme_name}' was not found in {self.themes_dir}.")
        with theme_path.open("r", encoding=FILE_ENCODING) as file:
            return json.load(file)

    def get_metadata(self, theme_name: str) -> ThemeMetadata:
        """Return display metadata and color tokens for a theme."""
        theme = self.load_theme(theme_name)
        colors = {
            key: str(value)
            for key, value in theme.items()
            if key not in {"name", "description"}
        }
        return ThemeMetadata(
            identifier=theme_name,
            name=str(theme.get("name", theme_name)),
            description=str(theme.get("description", "")),
            colors=colors,
        )
