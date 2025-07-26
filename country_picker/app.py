import sys, os, time
from html import escape
from typing import Optional, List
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from .fetcher import fetch_countries
from .style_loader import (
    load_stylesheet, 
    combo_custom_style,
    STYLESHEET_PATH,
    ICONS_DIR,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    Colors
)


class CountryWorker(QThread):
    countries_loaded = pyqtSignal(list)
    
    def run(self):
        time.sleep(1) # for testing
        try:
            success,data = fetch_countries()
            if not success:
                raise RuntimeError(data)
            self.countries_loaded.emit(data)
        except Exception as e:
            print(f"Error fetching countries: {e}")
            self.countries_loaded.emit([])


class CountryPickerApp(QWidget):
    """Main application window for country selection"""
    def __init__(self, initial_country: Optional[str] = None):
        """
        Initialize the main window
        
        Args:
            initial_country: Optional preselected country name
        """
        super().__init__()
        self.initial_country = initial_country
        
        self.init_ui()
        self.start_loading_countries()

    def init_ui(self):
        """Initialize the user interface components"""
        # Window configuration
        self.setWindowTitle("Country Picker")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'globe-icon.svg')))
        
        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(main_layout)
        
        # Create country picker section
        self.create_country_picker(main_layout)
        
        # Show initial loading state
        self.show_loading_message()

    def create_country_picker(self, parent_layout):
        """
        Create the country selection UI components
        
        Args:
            parent_layout: Layout to add the picker components to
        """
        # Create group box container
        picker_layout = QVBoxLayout()
        picker_layout.setContentsMargins(10, 20, 10, 10)
        
        group_box = QGroupBox("Country Picker")
        group_box.setLayout(picker_layout)
        parent_layout.addWidget(group_box)
        
        # Create and configure country dropdown
        self.country_combo = QComboBox()
        combo_custom_style(self.country_combo)
        self.country_combo.currentTextChanged.connect(self.update_selection_label)
        picker_layout.addWidget(self.country_combo)
        
        # Create selection display label
        self.selection_label = QLabel()
        self.selection_label.setTextFormat(1)  # Allows rendering of HTML-like text
        picker_layout.addWidget(self.selection_label)

    def show_loading_message(self):
        """Display loading state in in selection_label"""
        self.selection_label.setText(
            f"<span style='color: {Colors.LABEL};'>Loading countries...</span>"
        )

    def show_error(self, message: str):
        """Display error message in selection_label"""
        self.selection_label.setText(
            f"<span style='color: {Colors.ERROR};'>Error: {escape(message)}</span>"
        )
    
    def update_selection_label(self, country: str):
        """Display selected country in selection_label"""
        self.selection_label.setText(
            f"<span style='color: {Colors.LABEL};'>Selected:</span> "
            f"<span style='color: {Colors.COUNTRY}; font-weight: bold;'>"
            f"{escape(country)}"
            f"</span>"
        )

    def start_loading_countries(self):
        self.worker = CountryWorker()
        self.worker.countries_loaded.connect(self.populate_countries)
        self.worker.start()
        
    def populate_countries(self, countries: List[str]):
        """
        Populate the dropdown with country data
        
        Args:
            countries: List of country names to display
        """
        # Handle empty country list
        if not countries:
            self.show_error("No countries loaded")
            return
        
        self.country_combo.clear()
        self.country_combo.addItems(countries)
            
        # Set initial selection if specified
        if self.initial_country:
            normalized_initial = self.initial_country.lower()
            matches = [c for c in countries if c.lower() == normalized_initial]
            if matches:
                self.country_combo.setCurrentText(matches[0])
                return
            else:
                self.show_error(f"Initial country '{self.initial_country}' not found")

def run_app(initial_country: Optional[str] = None):
    """
    Run the country picker application
    
    Args:
        initial_country: Optional preselected country name
    """
    app = QApplication(sys.argv)
    load_stylesheet(app, STYLESHEET_PATH)
    
    window = CountryPickerApp(initial_country)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    """Entry point when run directly"""
    run_app()