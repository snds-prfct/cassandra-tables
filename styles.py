
BG_DARK      = "#1e1e2e"
BG_PANEL     = "#181825"
BG_EDITOR    = "#1e1e2e"
BG_TITLE_BAR = "#11111b"
ACCENT       = "#cba6f7"
TEXT_PRIMARY = "#cdd6f4"
TEXT_MUTED   = "#6c7086"
BORDER       = "#313244"
HIGHLIGHT    = "#313244"


STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG_DARK};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'SF Pro Text', 'Ubuntu', sans-serif;
    font-size: 13px;
}}

/* ── Splitter ── */
QSplitter::handle:horizontal {{
    background-color: {BORDER};
    width: 2px;
}}
QSplitter::handle:horizontal:hover,
QSplitter::handle:horizontal:pressed {{
    background-color: {ACCENT};
    width: 2px;
}}

/* ── Sidebar ── */
#sidebar {{
    background-color: {BG_PANEL};
    border-right: 1px solid {BORDER};
}}
#sidebarHeader {{
    background-color: {BG_PANEL};
    color: {TEXT_MUTED};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 10px 14px 6px 14px;
    border-bottom: 1px solid {BORDER};
}}
QTreeWidget {{
    background-color: {BG_PANEL};
    border: none;
    outline: none;
    padding: 4px 0;
}}
QTreeWidget::item {{
    padding: 3px 6px;
    border-radius: 4px;
    margin: 1px 4px;
    color: {TEXT_PRIMARY};
}}
QTreeWidget::item:hover    {{ background-color: {HIGHLIGHT}; }}
QTreeWidget::item:selected {{ background-color: #45475a; color: {TEXT_PRIMARY}; }}
QTreeWidget::branch        {{ background-color: transparent; }}

/* ── Tab widget ── */
QTabWidget::pane {{
    border: none;
    background-color: {BG_EDITOR};
}}
QTabBar {{
    background-color: {BG_PANEL};
}}
QTabBar::tab {{
    background-color: transparent;
    color: {TEXT_MUTED};
    padding: 7px 20px;
    border-top: 2px solid transparent;
    font-size: 13px;
}}
QTabBar::tab:selected {{
    background-color: {BG_EDITOR};
    color: {TEXT_PRIMARY};
    border-top: 2px solid {ACCENT};
}}
QTabBar::tab:hover:!selected {{
    background-color: {HIGHLIGHT};
    color: {TEXT_PRIMARY};
}}
QTabBar::close-button {{
    subcontrol-position: right;
}}

/* ── Top bar ── */
#topBar {{
    background-color: {BG_PANEL};
    border-bottom: 1px solid {BORDER};
}}
#topBarLabel {{
    color: {TEXT_MUTED};
    font-size: 12px;
    font-weight: 600;
    padding: 0 4px;
}}
QLineEdit {{
    background-color: {BG_DARK};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 13px;
    selection-background-color: #45475a;
}}
QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
QPushButton {{
    background-color: {ACCENT};
    color: {BG_DARK};
    border: none;
    border-radius: 4px;
    padding: 5px 16px;
    font-size: 13px;
    font-weight: 700;
}}
QPushButton:hover   {{ background-color: #d0b3ff; }}
QPushButton:pressed {{ background-color: #a882d4; }}

/* ── Grid cells ── */
#columnGridCell {{
    background-color: #a882d4;
    border: 1px solid {BORDER};
    border-radius: 4px;
    color: {TEXT_PRIMARY};
    font-size: 14px;
}}

#valueGridCell {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 4px;
    color: {TEXT_PRIMARY};
    font-size: 14px;
}}

/* ── Status bar ── */
QStatusBar {{
    background-color: {ACCENT};
    color: {BG_DARK};
    font-size: 12px;
    font-weight: 600;
    padding: 0 10px;
    min-height: 24px;
}}
QStatusBar::item {{ border: none; }}
"""
