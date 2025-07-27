"""
Country Picker Application

A PyQt5-based graphical application for selecting countries from a dynamically loaded list.
The application features asynchronous data loading, responsive UI, and customizable styling.
"""

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
    STYLESHEET_PATH,
    ICONS_DIR,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    Colors
)

class CountryWorker(QThread):
    """Background worker for fetching country data"""
    countries_loaded = pyqtSignal(list)
    
    def run(self):
        """Execute country fetching in background thread"""
        time.sleep(1)  # Simulate network delay for testing
        try:
            status, msg, data = fetch_countries()
            if not status:
                raise RuntimeError(msg)
            self.countries_loaded.emit(data)
        except Exception as e:
            print(f"Error fetching countries: {e}")
            self.countries_loaded.emit([])

class CountryPickerApp(QWidget):
    """Main application window for country selection"""
    def __init__(self, initial_country: Optional[str] = None):
        """
        Initialize country picker
        
        Args:
            initial_country: Optional preselected country name
        """
        super().__init__()
        self.initial_country = initial_country
        self.init_ui()
        self.start_loading_countries()

    def init_ui(self):
        """Create and configure UI components"""
        # Window setup
        self.setWindowTitle("Country Picker")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'globe-icon.svg')))
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)
        
        # Create country selection UI
        self.create_country_picker(main_layout)
        self.show_loading_message()

    def create_country_picker(self, parent_layout):
        """Build country selection dropdown and display"""
        # Group container
        picker_layout = QVBoxLayout()
        group_box = QGroupBox("Country Picker")
        group_box.setLayout(picker_layout)
        parent_layout.addWidget(group_box)
        
        # Country dropdown
        self.country_combo = QComboBox()
        self.country_combo.currentTextChanged.connect(self.update_selection_label)
        picker_layout.addWidget(self.country_combo)
        
        # Selection display
        self.selection_label = QLabel()
        self.selection_label.setTextFormat(1)  # Enable HTML-like text
        picker_layout.addWidget(self.selection_label)

    def show_loading_message(self):
        """Display loading indicator"""
        self.selection_label.setText(
            f"<span style='color: {Colors.LABEL};'>Loading countries...</span>"
        )

    def show_error(self, message: str):
        """Display error message in UI"""
        self.selection_label.setText(
            f"<span style='color: {Colors.ERROR};'>Error: {escape(message)}</span>"
        )
    
    def update_selection_label(self, country: str):
        """Update display with selected country"""
        self.selection_label.setText(
            f"<span style='color: {Colors.LABEL};'>Selected:</span> "
            f"<span style='color: {Colors.COUNTRY}; font-weight: bold;'>"
            f"{escape(country)}"
            f"</span>"
        )

    def start_loading_countries(self):
        """Start background country data loading"""
        self.worker = CountryWorker()
        self.worker.countries_loaded.connect(self.populate_countries)
        self.worker.start()
        
    def populate_countries(self, countries: List[str]):
        """
        Populate dropdown with country data
        
        Args:
            countries: List of country names to display
        """
        if not countries:
            self.show_error("No countries loaded")
            return
        
        self.country_combo.clear()
        self.country_combo.addItems(countries)
            
        # Set initial selection if provided
        if self.initial_country:
            normalized_initial = self.initial_country.lower()
            matches = [c for c in countries if c.lower() == normalized_initial]
            if matches:
                self.country_combo.setCurrentText(matches[0])
            else:
                self.show_error(f"Initial country '{self.initial_country}' not found")

def run_app(initial_country: Optional[str] = None):
    """
    Launch the country picker application
    
    Args:
        initial_country: Optional preselected country name
    """
    app = QApplication(sys.argv)
    load_stylesheet(app, STYLESHEET_PATH)
    
    window = CountryPickerApp(initial_country)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    """Direct execution entry point"""
    run_app()