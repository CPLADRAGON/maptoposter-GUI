from pathlib import Path


def test_windows_gui_launcher_uses_virtualenv_python():
    launcher = Path("run_gui.ps1").read_text(encoding="utf-8")

    assert ".venv\\Scripts\\python.exe" in launcher
    assert "-m maptoposter_gui.app" in launcher
