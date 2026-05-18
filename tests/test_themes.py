from maptoposter_core.themes import ThemeManager


def test_theme_manager_lists_builtin_themes():
    manager = ThemeManager()

    assert "terracotta" in manager.list_theme_names()


def test_theme_manager_loads_metadata():
    manager = ThemeManager()
    metadata = manager.get_metadata("terracotta")

    assert metadata.identifier == "terracotta"
    assert metadata.name == "Terracotta"
    assert metadata.colors["bg"] == "#F5EDE4"
    assert metadata.colors["road_motorway"] == "#A0522D"
