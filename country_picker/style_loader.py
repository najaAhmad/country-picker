import os, sys
from PyQt5.QtWidgets import QApplication, QComboBox

# Resource paths (using pathlib for better path handling)
ASSETS_DIR = os.path.join(os.path.abspath("."), __package__, 'assets')
STYLESHEET_DIR = os.path.join(ASSETS_DIR, "styles.qss")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")

# Window configuration
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 200

# Color palette
class Colors:
    LABEL = "#777777"      # Gray color for "Selected:" text
    COUNTRY = "#1e3a8a"    # Blue color for country name
    ERROR = "#cc0000"      # Red color for error messages


def load_stylesheet(app: QApplication, stylesheet_path: str) -> None:
    """
    Load and apply application stylesheet
    
    Args:
        app: QApplication instance to style
        stylesheet_path: Path to the QSS file
    """
    try:
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as f:
                app.setStyleSheet(f.read())
        else:
            print(f"Stylesheet not found at {stylesheet_path}, using default styling", 
                  file=sys.stderr)
    except Exception as e:
        print(f"Error loading stylesheet: {e}")

def combo_custom_style(combo:QComboBox):
    """Apply custom styling to the dropdown combobox"""
    try:
        combo.setStyleSheet(f"""
            QComboBox::down-arrow {{
                image: url({os.path.join(ICONS_DIR, 'down-arrow.svg')});
                width: 25px;
                height: 25px;
            }}
        """)
    except Exception as e:
        print(f"Error styling QComboBox: {e}")