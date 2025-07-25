"""
PyQt5 Country Picker Application

This module provides a GUI application for selecting countries from a dropdown list.
The country data is fetched asynchronously from a network source.

Features:
- Asynchronous country data loading
- Customizable styling via CSS
- Responsive UI with loading states
- Custom icons for window and dropdown
- Initial country selection support
- Different colors for label text and country value
"""

import sys
import os
from html import escape
from typing import Optional, List
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from importlib.resources import files


class WorkerThread(QThread):
    """QThread subclass for fetching country data in the background"""
    
    def __init__(self, fetcher):
        """
        Initialize the worker thread
        
        Args:
            fetcher: CountryFetcher instance that handles network operations
        """
        super().__init__()
        self.fetcher = fetcher

    def run(self):
        """Execute the country fetching operation"""
        self.fetcher.fetch_countries()


class MainWindow(QWidget):
    """Main application window for country selection"""
    
    # Window configuration constants
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 200
    LAYOUT_MARGINS = 30
    PICKER_MARGINS = (10, 20, 10, 10)
    ICON_SIZE = 16  # Size for dropdown arrow icon
    
    # Color constants for text formatting
    LABEL_COLOR = "#777777"  # Gray color for "Selected:" text
    COUNTRY_COLOR = "#1e3a8a"  # Blue color for country name
    ERROR_COLOR = "#cc0000"  # Red color for error messages

    def __init__(self, initial_country: Optional[str] = None):
        """
        Initialize the main window
        
        Args:
            initial_country: Optional preselected country name
        """
        super().__init__()
        self.initial_country = initial_country
        self.fetcher = None
        self.thread = None
        
        self.init_ui()
        self.start_worker()

    def init_ui(self):
        """Initialize the user interface components"""
        # Window configuration
        self.setWindowTitle("Country Picker")
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            self.LAYOUT_MARGINS, 
            self.LAYOUT_MARGINS, 
            self.LAYOUT_MARGINS, 
            self.LAYOUT_MARGINS
        )
        self.setLayout(main_layout)
        
        # Set window icon
        self.set_window_icon()
        
        # Create country picker section
        self.create_country_picker(main_layout)
        
        # Show initial loading state
        self.show_loading_message()

    def set_window_icon(self):
        """Set the application window icon"""
        try:
            icon_path = str(files('country_picker.icons').joinpath('globe-icon.svg'))
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"Error loading window icon: {e}", file=sys.stderr)

    def create_country_picker(self, parent_layout):
        """
        Create the country selection UI components
        
        Args:
            parent_layout: Layout to add the picker components to
        """
        # Create group box container
        picker_layout = QVBoxLayout()
        picker_layout.setContentsMargins(*self.PICKER_MARGINS)
        
        group_box = QGroupBox("Country Picker")
        group_box.setLayout(picker_layout)
        parent_layout.addWidget(group_box)
        
        # Create and configure country dropdown
        self.country_combo = QComboBox()
        self.style_dropdown()
        self.country_combo.currentTextChanged.connect(self.update_selection_label)
        picker_layout.addWidget(self.country_combo)
        
        # Create selection display label
        self.selection_label = QLabel()
        self.selection_label.setTextFormat(1)  # Enable rich text formatting
        picker_layout.addWidget(self.selection_label)

    def style_dropdown(self):
        """Apply custom styling to the dropdown combobox"""
        try:
            arrow_icon_path = str(files('country_picker.icons').joinpath('down-arrow.svg'))
            self.country_combo.setStyleSheet(f"""
                QComboBox::down-arrow {{
                    image: url({arrow_icon_path});
                    width: {self.ICON_SIZE}px;
                    height: {self.ICON_SIZE}px;
                }}
            """)
        except Exception as e:
            print(f"Error styling dropdown: {e}", file=sys.stderr)

    def show_loading_message(self):
        """Display loading state in the UI"""
        self.selection_label.setText(
            f"<span style='color: {self.LABEL_COLOR};'>Loading countries...</span>"
        )

    def show_error(self, message: str):
        """
        Display error message in the UI with error color
        
        Args:
            message: Error message to display
        """
        self.selection_label.setText(
            f"<span style='color: {self.ERROR_COLOR};'>Error: {escape(message)}</span>"
        )

    def start_worker(self):
        """Initialize and start the country data fetching thread"""
        from .network import CountryFetcher  # Local import to prevent circular dependency
        
        self.fetcher = CountryFetcher()
        self.fetcher.data_ready.connect(self.populate_country_dropdown)
        self.fetcher.error_occurred.connect(self.show_error)
        
        self.thread = WorkerThread(self.fetcher)
        self.thread.start()

    def populate_country_dropdown(self, countries: List[str]):
        """
        Populate the dropdown with country data
        
        Args:
            countries: List of country names to display
        """
        self.country_combo.clear()
        self.country_combo.addItems(countries)
        
        # Handle empty country list
        if not countries:
            self.show_error("No countries loaded")
            return
            
        # Set initial selection if specified
        if self.initial_country:
            normalized_initial = self.initial_country.lower()
            matches = [c for c in countries if c.lower() == normalized_initial]
            if matches:
                self.country_combo.setCurrentText(matches[0])
                self.update_selection_label(matches[0])
                return
        
        # Default to first country
        self.update_selection_label(countries[0])

    def update_selection_label(self, country: str):
        """
        Update the selection display label with different colors for label and value
        
        Args:
            country: Currently selected country name
        """
        # Use HTML formatting to apply different colors
        self.selection_label.setText(
            f"<span style='color: {self.LABEL_COLOR};'>Selected:</span> "
            f"<span style='color: {self.COUNTRY_COLOR}; font-weight: bold;'>"
            f"{escape(country)}"
            f"</span>"
        )


def run_app(initial_country: Optional[str] = None):
    """
    Run the country picker application
    
    Args:
        initial_country: Optional preselected country name
    """
    app = QApplication(sys.argv)
    load_stylesheet(app)
    
    window = MainWindow(initial_country)
    window.show()
    
    sys.exit(app.exec_())


def load_stylesheet(app: QApplication):
    """
    Load and apply application stylesheet
    
    Args:
        app: QApplication instance to style
    """
    try:
        css_path = str(files('country_picker').joinpath("style.qss"))
        if os.path.exists(css_path):
            with open(css_path, "r") as f:
                app.setStyleSheet(f.read())
            print("Stylesheet loaded successfully")
        else:
            print("Stylesheet not found, using default styling", file=sys.stderr)
    except Exception as e:
        print(f"Error loading stylesheet: {e}", file=sys.stderr)


if __name__ == "__main__":
    """Entry point when run directly"""
    run_app()