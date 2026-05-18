from maptoposter_gui import style


def test_dark_stylesheet_uses_dark_mode_tokens_without_pure_black_or_white_text():
    sheet = style.build_stylesheet()

    assert style.APP_BG in sheet
    assert style.SURFACE_1 in sheet
    assert style.SURFACE_2 in sheet
    assert style.TEXT_PRIMARY in sheet
    assert style.ACCENT in sheet
    assert "#000000" not in sheet
    assert "#FFFFFF" not in sheet
    assert ":focus" in sheet
