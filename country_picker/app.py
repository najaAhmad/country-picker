import sys
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QLabel
)
from PyQt5.QtCore import QThread
from .network import CountryFetcher

class WorkerThread(QThread):
    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher

    def run(self):
        self.fetcher.fetch_countries()

class MainWindow(QWidget):
    def __init__(self, initial_country: str = None):
        super().__init__()
        self.initial_country = initial_country
        self.init_ui()
        self.start_worker()

    def init_ui(self):
        self.setWindowTitle("Country Picker")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setFixedSize(400, 120)
        
        self.combobox = QComboBox()
        self.combobox.currentTextChanged.connect(self.update_label)
        layout.addWidget(self.combobox)
        
        self.label = QLabel("Selected: ")
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        # self.resize(500, 200)
        self.show_loading_message()

    def show_loading_message(self):
        self.label.setText("Loading countries...")

    def show_error(self, message: str):
        self.label.setText(f"Error: {message}")

    def start_worker(self):
        self.fetcher = CountryFetcher()
        self.fetcher.data_ready.connect(self.populate_combobox)
        self.fetcher.error_occurred.connect(self.show_error)
        
        self.thread = WorkerThread(self.fetcher)
        self.thread.start()

    def populate_combobox(self, countries: list):
        self.combobox.clear()
        self.combobox.addItems(countries)
        
        if not countries:
            self.show_error("No countries loaded")
            return
            
        if self.initial_country:
            matches = [c for c in countries if c.lower() == self.initial_country.lower()]
            if matches:
                self.combobox.setCurrentText(matches[0])
                self.update_label(matches[0])
                return
        
        self.update_label(countries[0])

    def update_label(self, country: str):
        self.label.setText(f"Selected: {country}")


def run_app(initial_country: Optional[str] = None):
    app = QApplication(sys.argv)

    window = MainWindow(initial_country)
    window.show()
    sys.exit(app.exec_())