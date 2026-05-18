"""Dark-mode-first style tokens and Qt stylesheet."""

APP_BG = "#101214"
SURFACE_1 = "#171A1F"
SURFACE_2 = "#20242B"
SURFACE_3 = "#2A3038"
TEXT_PRIMARY = "#E6E8EB"
TEXT_SECONDARY = "#AEB6C2"
TEXT_MUTED = "#737D8C"
BORDER = "#303640"
ACCENT = "#7BB7C7"
ACCENT_PRESSED = "#5B9BAB"
SUCCESS = "#7AC29A"
WARNING = "#D9B66F"
ERROR = "#E07A7A"


def build_stylesheet() -> str:
    """Build the application stylesheet using dark-mode semantic tokens."""
    return f"""
    QMainWindow, QWidget {{
        background: {APP_BG};
        color: {TEXT_PRIMARY};
        font-family: Segoe UI, Arial, sans-serif;
        font-size: 13px;
    }}
    QGroupBox {{
        background: {SURFACE_1};
        border: 1px solid {BORDER};
        border-radius: 14px;
        margin-top: 18px;
        padding: 14px;
        color: {TEXT_PRIMARY};
        font-weight: 600;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 6px;
        color: {TEXT_SECONDARY};
    }}
    QLabel {{
        color: {TEXT_SECONDARY};
        background: transparent;
    }}
    QLabel#HeroTitle {{
        color: {TEXT_PRIMARY};
        font-size: 22px;
        font-weight: 700;
    }}
    QLabel#MutedLabel {{
        color: {TEXT_MUTED};
    }}
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background: {SURFACE_2};
        border: 1px solid {BORDER};
        border-radius: 9px;
        color: {TEXT_PRIMARY};
        padding: 8px 10px;
        selection-background-color: {ACCENT};
        selection-color: {APP_BG};
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 1px solid {ACCENT};
    }}
    QComboBox::drop-down {{
        border: 0;
        width: 28px;
    }}
    QComboBox QAbstractItemView {{
        background: {SURFACE_3};
        border: 1px solid {BORDER};
        selection-background-color: {ACCENT};
        selection-color: {APP_BG};
        color: {TEXT_PRIMARY};
    }}
    QPushButton {{
        background: {SURFACE_2};
        border: 1px solid {BORDER};
        border-radius: 10px;
        color: {TEXT_PRIMARY};
        padding: 9px 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background: {SURFACE_3};
        border-color: {ACCENT};
    }}
    QPushButton:focus {{
        border: 1px solid {ACCENT};
    }}
    QPushButton#PrimaryButton {{
        background: {ACCENT};
        color: {APP_BG};
        border-color: {ACCENT};
    }}
    QPushButton#PrimaryButton:hover {{
        background: #90CAD8;
    }}
    QPushButton#PrimaryButton:pressed {{
        background: {ACCENT_PRESSED};
    }}
    QPushButton#DangerButton {{
        color: {ERROR};
        border-color: rgba(224, 122, 122, 0.45);
    }}
    QPushButton:disabled {{
        color: {TEXT_MUTED};
        background: {SURFACE_1};
        border-color: {BORDER};
    }}
    QProgressBar {{
        background: {SURFACE_2};
        border: 1px solid {BORDER};
        border-radius: 8px;
        color: {TEXT_SECONDARY};
        text-align: center;
        min-height: 18px;
    }}
    QProgressBar::chunk {{
        background: {ACCENT};
        border-radius: 7px;
    }}
    QScrollArea {{
        background: transparent;
        border: none;
    }}
    QToolTip {{
        background: {SURFACE_3};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        padding: 6px;
        border-radius: 6px;
    }}
    """
