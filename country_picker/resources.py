# country_picker/resources.py
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (pyinstaller)
        base_path = sys._MEIPASS
    else:
        # If it's run as a normal Python script
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)