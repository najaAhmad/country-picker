# Country Picker Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) 
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **PyQt5** desktop application that displays countries fetched from a REST API in a combobox with real-time selection updates.

---

## ✨ Features

- 🌐 Fetches country data from REST API in a background thread  
- 🔠 Displays alphabetically sorted country list in a combobox  
- 🖥️ Real-time country selection display in a label  
- 🧵 Thread-safe UI updates (main thread only)  
- ⚙️ CLI argument for preset country selection  
- ✅ Unit tests for data parsing logic  
- 📦 Modular package structure  
- 🧩 Type hints and docstrings throughout  

---

## 📦 Installation

**Clone repository:**

```bash
git clone https://github.com/yourusername/country-picker.git
cd country-picker
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

**Basic usage:**

```bash
python -m country_picker
```

**Preselect a country:**

```bash
python -m country_picker --select "Switzerland"
```

---

## 🗂️ Project Structure

```
pyqt5-country-picker/
├── assets/
│   ├── icons/              # Country flag images (200+)
│   │   ├── down-arrow.svg
│   │   └── globe-icon.svg
│   └── styles/
│       └── style.qss       # Application stylesheet
│
├── country_picker/
│   ├── __init__.py
│   ├── __main__.py         # CLI interface
│   ├── app.py              # Main application/GUI logic
│   ├── fetcher.py          # Data fetching and parsing
│   └── style_loader.py     # Stylesheet loader
│
├── tests/
│   ├── __init__.py
│   └── test_fetcher.py     # JSON parsing tests
│
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```

---

## ✅ Testing

Run unit tests:

```bash
python3 -m unittest discover country_picker.tests
```

**Sample output:**

```
Ran 3 tests in 0.002s

OK
```

---

## 🔧 Implementation Notes

### 🧵 Thread Management

- Background thread for network operations  
- Main-thread-only UI updates using Qt signals  
- Automatic thread cleanup  

### ❗ Error Handling

- Network request timeout (10 seconds)  
- JSON parsing validation  
- Graceful degradation on API failure  

### 🧹 Code Quality

- PEP-8 compliant  
- Type hints for all functions  
- Comprehensive docstrings  
- Configurable API endpoint  

---

## 🌍 API Endpoint

This app uses:  
[`https://www.apicountries.com/countries`](https://www.apicountries.com/countries)

```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.