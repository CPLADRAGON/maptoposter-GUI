"""Compatibility exports for data-fetching helpers.

The GUI currently uses :class:`maptoposter_core.generator.MapPosterGenerator`, which
keeps the proven legacy fetching/rendering code in place. These exports provide a
stable module boundary for future deeper refactoring.
"""

from create_map_poster import CacheError, cache_get, cache_set, fetch_features, fetch_graph, get_coordinates

__all__ = [
    "CacheError",
    "cache_get",
    "cache_set",
    "fetch_features",
    "fetch_graph",
    "get_coordinates",
]
